#!/usr/bin/env python3
"""Tell IndexNow which pages changed.

IndexNow is a shared feed: one request reaches Bing, Yandex, Naver, Seznam and
Yep, and Bing's index is what ChatGPT search and Microsoft Copilot lean on.
Google does not take part. It finds changes through sitemap.xml instead.

The key is not a secret. It is the name of a text file at the site root, which
is how the search engines check that the request really comes from this site.

  python3 scripts/indexnow.py --before <sha> --after <sha>   # what one push changed
  python3 scripts/indexnow.py --all                          # every page in the sitemap
  add --dry-run to print the addresses without sending anything
  add --wait-for-deploy to hold until Cloudflare Pages has published the push

Only addresses listed in sitemap.xml are ever sent, so utility pages (the 404
page, thank-you pages, anything robots.txt keeps private) can never be
submitted by accident. The one exception is a page a push deleted: it is sent
once, so the search engines learn it is gone.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent

# --- This site ---------------------------------------------------------------
HOST = "mybusinessfeedback.com"
KEY_DIR = REPO              # the folder whose files are served from the site root
PAGES_IN_REPO = True        # every page is an index.html committed here, so a push is narrowed to the pages it touched
SITE_PATHS: tuple = ()      # only used where pages are built rather than committed
SITE_FILES: frozenset = frozenset()
WORKFLOW_FILE = ".github/workflows/indexnow.yml"
# ------------------------------------------------------------------------------

# Overridable so the script can be tested without touching the live services.
# The INDEXNOW_* names are read only by the tests; nothing sets them in normal use.
SITE = os.environ.get("INDEXNOW_SITE", f"https://{HOST}").rstrip("/")
ENDPOINT = os.environ.get("INDEXNOW_ENDPOINT", "https://api.indexnow.org/indexnow")
GITHUB_API = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
POLL_SECONDS = float(os.environ.get("INDEXNOW_POLL_SECONDS", "15"))

KEY_RE = re.compile(r"^[a-f0-9]{32}$")
CLOUDFLARE_APP = "cloudflare-workers-and-pages"
AGENT = f"indexnow-notify/1.0 (+https://{HOST}/)"


def find_key() -> tuple[str, str]:
    """The key and the path of its file inside the repo."""
    for path in sorted(KEY_DIR.glob("*.txt")):
        if KEY_RE.match(path.stem) and path.read_text(encoding="utf-8").strip() == path.stem:
            return path.stem, path.relative_to(REPO).as_posix()
    sys.exit(f"No IndexNow key file in {KEY_DIR.relative_to(REPO).as_posix() or '.'}/.")


def fetch(url: str, headers: dict | None = None, timeout: int = 25) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": AGENT, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status, res.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


def git(*args: str) -> str:
    done = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=False)
    return done.stdout if done.returncode == 0 else ""


def have_commit(sha: str) -> bool:
    done = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=REPO,
                          capture_output=True, check=False)
    return done.returncode == 0


def ensure_commit(sha: str) -> bool:
    """A shallow checkout holds one commit. Fetch the other side of the diff."""
    if have_commit(sha):
        return True
    subprocess.run(["git", "fetch", "--no-tags", "--depth=1", "origin", sha], cwd=REPO,
                   capture_output=True, check=False)
    return have_commit(sha)


def locs(xml: str) -> list[str]:
    return re.findall(r"<loc>\s*(https://%s/[^<\s]*)\s*</loc>" % re.escape(HOST), xml)


def live_sitemap() -> list[str]:
    status, xml = fetch(f"{SITE}/sitemap.xml")
    return locs(xml) if status == 200 else []


def page_url(name: str) -> str | None:
    if name == "index.html":
        return f"https://{HOST}/"
    if name.endswith("/index.html"):
        return f"https://{HOST}/{name[:-len('index.html')]}"
    return None


def changed_files(before: str, after: str) -> list[tuple[str, str]] | None:
    """(status, path) for every file a push touched. None when it cannot be told."""
    if not (ensure_commit(before) and ensure_commit(after)):
        return None
    done = subprocess.run(["git", "diff", "--name-status", "--no-renames", before, after],
                          cwd=REPO, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        return None
    rows = []
    for line in done.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) == 2:
            rows.append((parts[0].strip(), parts[1].strip()))
    return rows


def wait_for_cloudflare(sha: str) -> None:
    """Hold until Cloudflare Pages reports the push as published.

    Cloudflare posts a check on each commit it deploys. What ends up live is
    the newest commit on main, which is not always the pushed one: the
    AI-crawler workflow commits regenerated files a few seconds after a content
    push, and Cloudflare then builds that commit and can leave the check on the
    pushed one unfinished for good. So the newest commit is the one to watch.
    If it never gets a check at all (a commit marked to skip the build), the
    pushed commit being live is enough. Running out of time is not an error:
    the addresses are sent anyway.
    """
    minutes = float(os.environ.get("INDEXNOW_WAIT_MINUTES", "10"))
    follow_minutes = float(os.environ.get("INDEXNOW_FOLLOW_MINUTES", "1.5"))
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not (repo and token and sha):
        print("No GitHub details to watch the deploy with. Waiting two and a half minutes instead.")
        time.sleep(float(os.environ.get("INDEXNOW_FALLBACK_SECONDS", "150")))
        return
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    def cloudflare_check(ref: str) -> str:
        """'none', 'running', 'success' or 'failure' for the Cloudflare check on a commit."""
        status, body = fetch(f"{GITHUB_API}/repos/{repo}/commits/{ref}/check-runs?per_page=100", headers)
        if status != 200:
            return "none"
        try:
            runs = json.loads(body).get("check_runs", [])
        except ValueError:
            return "none"
        mine = [r for r in runs if (r.get("app") or {}).get("slug") == CLOUDFLARE_APP]
        if not mine:
            return "none"
        if any(r.get("status") != "completed" for r in mine):
            return "running"
        return "failure" if any(r.get("conclusion") == "failure" for r in mine) else "success"

    def head_of_main() -> str:
        status, body = fetch(f"{GITHUB_API}/repos/{repo}/commits/main", headers)
        try:
            return json.loads(body).get("sha", "") if status == 200 else ""
        except ValueError:
            return ""

    started = time.time()
    pushed_live_since = None
    while True:
        head = head_of_main() or sha
        pushed = cloudflare_check(sha)
        newest = pushed if head == sha else cloudflare_check(head)
        if newest == "failure":
            sys.exit("Cloudflare Pages reports that the deploy failed, so nothing was sent.")
        if newest == "success":
            print("Cloudflare Pages has published this push." if head == sha
                  else "Cloudflare Pages has published this push and the commit that followed it.")
            return
        if pushed == "success":
            # The push is live. A newer commit is on main: wait while Cloudflare is
            # building it, but not for one it shows no sign of building.
            pushed_live_since = pushed_live_since or time.time()
            if newest == "none" and time.time() - pushed_live_since > follow_minutes * 60:
                print("Cloudflare Pages has published this push. The commit after it is not being built.")
                return
        if time.time() - started > minutes * 60:
            print(f"No word from Cloudflare Pages after {minutes:g} minutes. Carrying on.")
            return
        time.sleep(POLL_SECONDS)


def wait_for_key(key: str, minutes: float) -> bool:
    """On the first run, the key file going live is also the sign the deploy has finished."""
    url = f"{SITE}/{key}.txt"
    deadline = time.time() + minutes * 60
    while True:
        status, text = fetch(url)
        if status == 200 and text.strip() == key:
            return True
        if time.time() > deadline:
            return False
        time.sleep(POLL_SECONDS)


def send(key: str, urls: list[str]) -> None:
    body = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }).encode("utf-8")
    tries = int(os.environ.get("INDEXNOW_TRIES", "4"))
    pause = float(os.environ.get("INDEXNOW_RETRY_SECONDS", "60"))
    pending = False
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8",
                                              "User-Agent": AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                status = res.status
            if status != 202:
                print(f"IndexNow answered {status}. The addresses were received.")
                return
            # 202 means the addresses arrived before IndexNow had checked the
            # key file, which is what a key gets the first time it is used.
            # Bing Webmaster Tools never listed a batch answered that way, and
            # listed the same batch at once when it was sent again minutes
            # later and answered 200. So a 202 is sent again after a pause.
            pending = True
            problem = "202, received before the key file was checked"
        except urllib.error.HTTPError as err:
            # 403 means IndexNow could not read the key file. Straight after a
            # deploy that is usually a matter of seconds, while the file reaches
            # the part of the network IndexNow checks from. 429 and 5xx pass too.
            pending = False
            problem = f"{err.code} {err.reason}"
            if not (err.code in (403, 429) or err.code >= 500):
                sys.exit(f"IndexNow refused the request: {problem}")
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            pending = False
            problem = f"no answer ({err})"
        if attempt < tries:
            wait = pause * attempt
            print(f"IndexNow said {problem}. Trying again in {wait:g} seconds ({attempt} of {tries}).")
            time.sleep(wait)
    if pending:
        print(f"IndexNow still answered 202 after {tries} tries. The addresses were received, but the key file "
              "had not been checked by then, so Bing may not list them. Running this workflow by hand sends "
              "every page again.")
        return
    sys.exit(f"IndexNow refused the request: {problem}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", default="")
    ap.add_argument("--after", default="HEAD")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wait-for-deploy", action="store_true",
                    help="hold until Cloudflare Pages has published the push")
    ap.add_argument("--wait", type=int, default=0, help="seconds to wait first")
    args = ap.parse_args()

    key, key_file = find_key()
    no_before = not args.before or set(args.before) == {"0"}
    everything = args.all or no_before
    picked: list[str] = []     # pages this push edited or added
    removed: list[str] = []    # pages this push deleted

    if not everything:
        touched = changed_files(args.before, args.after)
        names = {name for _, name in touched or []}
        if touched is None:
            # The two commits could not be compared, so err on the side of telling.
            print("This push could not be compared with the one before it, so every page is sent.")
            everything = True
        elif key_file in names or WORKFLOW_FILE in names:
            # The key or the workflow arriving means IndexNow has just been set up or changed here.
            print("The IndexNow setup changed in this push, so every page is sent once.")
            everything = True
        elif not PAGES_IN_REPO:
            if any(name.startswith(SITE_PATHS) or name in SITE_FILES for name in names):
                everything = True
            else:
                print("This push changed no page, so there is nothing to send.")
                return
        else:
            old_listed = set(locs(git("show", f"{args.before}:sitemap.xml")))
            for status, name in touched:
                url = page_url(name) if name.endswith(".html") else None
                if not url:
                    continue
                if status == "D":
                    if url in old_listed:
                        removed.append(url)
                else:
                    picked.append(url)
            if not picked and not removed:
                print("This push changed no page, so there is nothing to send.")
                return

    if args.dry_run:
        if everything:
            print("Would send every page in the live sitemap.")
        for u in sorted(set(picked)):
            print("  changed  " + u)
        for u in sorted(set(removed)):
            print("  removed  " + u)
        return

    if args.wait:
        time.sleep(args.wait)
    if args.wait_for_deploy:
        wait_for_cloudflare(args.after if args.after != "HEAD" else os.environ.get("GITHUB_SHA", ""))
    if not wait_for_key(key, minutes=float(os.environ.get("INDEXNOW_KEY_MINUTES", "6"))):
        sys.exit(f"https://{HOST}/{key}.txt is not live, so nothing was sent.")

    listed = live_sitemap()
    if not listed:
        sys.exit(f"https://{HOST}/sitemap.xml could not be read, so nothing was sent.")
    if everything:
        urls = listed
    else:
        allowed = set(listed)
        sitemap_file = REPO / "sitemap.xml"
        if sitemap_file.is_file():
            allowed |= set(locs(sitemap_file.read_text(encoding="utf-8")))
        urls = sorted({u for u in picked if u in allowed} | set(removed))

    print(f"{len(urls)} address(es) to send:")
    for u in urls:
        print("  " + u)
    if not urls:
        return
    send(key, urls)


if __name__ == "__main__":
    main()
