# Nexus Multimedia Feedback Page: Apps Script Setup

The feedback page at `/nexusmultimedia/` is live and sends data to the shared MBF Apps Script backend. The backend CONFIG must be updated to route Nexus Multimedia submissions to the correct Google Sheet and notification email.

## 1. Update CONFIG.CLIENT_SHEETS

In the Apps Script editor, find the `CONFIG` object. Add the Nexus Multimedia sheet ID:

**Before:**
```javascript
const CONFIG = {
  CLIENT_SHEETS: {
    "kitsaplaw": "EXISTING_SHEET_ID",
    "hemeoncall": "EXISTING_SHEET_ID",
    "2hlaw": "EXISTING_SHEET_ID"
  },
```

**After:**
```javascript
const CONFIG = {
  CLIENT_SHEETS: {
    "kitsaplaw": "EXISTING_SHEET_ID",
    "hemeoncall": "EXISTING_SHEET_ID",
    "2hlaw": "EXISTING_SHEET_ID",
    "nexusmultimedia": "1ayvX2dLl8sZvW94WXmtClCOhATdmcMEErJFFnxd8Klw"
  },
```

## 2. Update CONFIG.CLIENT_NOTIFICATION_EMAILS

Add the notification email for Nexus Multimedia:

**Before:**
```javascript
  CLIENT_NOTIFICATION_EMAILS: {
    "kitsaplaw": "info@kitsaplawgroup.com",
    "hemeoncall": "info@hemeoncall.com",
    "2hlaw": "info@2hlaw.com"
  }
```

**After:**
```javascript
  CLIENT_NOTIFICATION_EMAILS: {
    "kitsaplaw": "info@kitsaplawgroup.com",
    "hemeoncall": "info@hemeoncall.com",
    "2hlaw": "info@2hlaw.com",
    "nexusmultimedia": "div@nexusmultimedia.ai"
  }
```

## 3. Deploy the updated script

1. In the Apps Script editor, click **Deploy > Manage deployments**
2. Click the pencil icon to edit the existing deployment
3. Set version to **New version**
4. Click **Deploy**

The existing Web App URL stays the same. No frontend changes needed.

## 4. Prepare the Google Sheet

Open the Nexus Multimedia feedback sheet (ID: `1ayvX2dLl8sZvW94WXmtClCOhATdmcMEErJFFnxd8Klw`).

Ensure Row 1 has these column headers (matching the payload fields):
- A: Timestamp
- B: Client ID
- C: Client Name
- D: Star Rating
- E: Path Taken
- F: Customer Name
- G: Customer Email
- H: Customer Phone
- I: Feedback Text
- J: Google Review Clicked
- K: Page URL
- L: User Agent

## 5. Upload the logo

Place `nexus-logo.png` in the `/nexusmultimedia/` folder in the repo, then commit and push:
```bash
cd ~/Desktop/mybusinessfeedback
cp /path/to/nexus-logo.png nexusmultimedia/nexus-logo.png
git add nexusmultimedia/nexus-logo.png
git commit -m "Add Nexus Multimedia logo"
git push origin main
```

## 6. Test

1. Visit: https://mybusinessfeedback.com/nexusmultimedia/
2. Verify the logo loads and the page renders correctly
3. Click 5 stars: should redirect to Google review page for Place ID `ChIJA9sSQhVZlWARgg665txsT0E`
4. Click 3 or 4 stars: should show feedback form
5. Click 1 or 2 stars: should show apology + direct contact (div@nexusmultimedia.ai, (619) 307-5951)
6. Submit a test feedback entry and verify it appears in the Google Sheet
7. Verify the notification email arrives at div@nexusmultimedia.ai
