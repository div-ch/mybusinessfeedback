# My Business Feedback

Customer feedback routing service for businesses. Captures post-service feedback, routes five-star customers to leave public Google reviews, and sends unhappy customers to a private channel with the business team.

## Folder Structure

```
/index.html              Public homepage
/robots.txt              Search engine directives
/.gitignore              Git ignore rules
/favicon.ico             Site favicon (to be added)
/[clientname]/           Client feedback pages (one folder per business)
/_template/              Template files for new client pages (not indexed)
```

## Deployment

- Hosted on Cloudflare Pages
- Auto-deploys on push to `main` branch on GitHub
- Domain: mybusinessfeedback.com
- Single-file HTML pages, no build step, no frameworks

## Tech Stack

- Pure HTML, CSS, vanilla JS
- Google Fonts: Fraunces (headings), Instrument Sans (body)
- Motion library via CDN for animations
- Google Apps Script for form submissions
- GA4 for analytics

## Design System

- Background: warm cream #FAF8F3
- Surface: white #FFFFFF
- Primary text: #1A1A1A
- Secondary text: #6B6B68
- Border: warm beige #E8E4DB
- Accent: deep forest green #1A4D3C
- Typography: Fraunces (serif, headings), Instrument Sans (sans, body)
