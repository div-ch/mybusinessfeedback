# Referral Tracking: Apps Script Update Instructions

The Partner-with-us form now includes a hidden `referred_by` field populated from the `mbf_ref` cookie. This cookie is set when any visitor lands on the site with a `?ref=NAME` URL parameter and persists for 30 days.

## 1. Add "Referred By" column to the Nexus MBF Leads sheet

Open the Google Sheet (ID: `1CSxXmu16n79Vwa3NdS7UUPSe2TJ7rc2rTOFRuLDkPKA`).

Add a new column header **"Referred By"** in the first available column after your existing headers.

## 2. Update the Apps Script doPost function

In the existing `doPost(e)` function, find where the incoming data is parsed and the row is appended. Add `referred_by` to the row data:

```javascript
// After parsing the POST body:
var data = JSON.parse(e.postData.contents);

// Add this line where you read the other fields:
var referredBy = data.referred_by || 'Direct (no referrer)';

// In your sheet.appendRow() call, add referredBy at the end:
sheet.appendRow([
  data.timestamp,
  data.business_name,
  data.contact_name,
  data.email,
  data.phone,
  data.website,
  data.business_type,
  data.message,
  data.page_url,
  referredBy       // <-- new field
]);
```

## 3. Update the notification email

Find the section that sends a notification email (likely using `MailApp.sendEmail` or `GmailApp.sendEmail`). Add the referral source to the email body:

```javascript
var emailBody = '... existing fields ...\n'
  + 'Referred by: ' + referredBy + '\n';
```

## 4. Deploy the updated script

1. In the Apps Script editor, click Deploy > Manage deployments
2. Edit the existing deployment
3. Set version to "New version"
4. Click Deploy

The existing Web App URL stays the same. No frontend changes needed.

## 5. Test

1. Visit: `https://mybusinessfeedback.com/partner-with-us/?ref=test`
2. Verify "Referred by test" appears below the form heading (subtle italic text)
3. Inspect the hidden input: `<input type="hidden" name="referred_by" id="referred_by" value="test">`
4. Submit a test form entry
5. Check the Google Sheet for the "Referred By" column showing "test"
6. Check your email notification includes "Referred by: test"

## 6. How referral links work

Sales agents share links like:
- `https://mybusinessfeedback.com/?ref=cody`
- `https://mybusinessfeedback.com/for-law-firms/?ref=sarah`
- `https://mybusinessfeedback.com/locations/new-york/law-firms/?ref=div`

The `?ref=` value is captured into a 30-day cookie on any page. When the visitor eventually reaches the Partner-with-us form (even days later), the cookie value is attached to the submission.

If no `?ref=` parameter was ever present, the field submits as an empty string and the Apps Script writes "Direct (no referrer)".
