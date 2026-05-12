# The Long Walk — Google Sheets Setup

Submissions from the interest form go straight to a Google Sheet. Here's how to set it up (5 minutes).

## Step 1: Create the Sheet

1. Go to [sheets.google.com](https://sheets.google.com) and create a new spreadsheet
2. Name it something like "Long Walk — Interest"
3. In Row 1, add these headers in columns A–D:
   - **A1:** Timestamp
   - **B1:** Name
   - **C1:** Email
   - **D1:** Handicap

## Step 2: Add the Apps Script

1. In the sheet, go to **Extensions → Apps Script**
2. Delete any code in the editor
3. Paste this:

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    data.timestamp || new Date().toISOString(),
    data.name || '',
    data.email || '',
    data.handicap || ''
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

4. Click **Save** (Ctrl+S / Cmd+S)

## Step 3: Deploy as Web App

1. Click **Deploy → New deployment**
2. Click the gear icon next to "Select type" → choose **Web app**
3. Set:
   - **Description:** Long Walk interest form
   - **Execute as:** Me
   - **Who has access:** Anyone
4. Click **Deploy**
5. Authorize when prompted (click through the "unsafe" warning — it's your own script)
6. Copy the **Web app URL** — it looks like `https://script.google.com/macros/s/ABC.../exec`

## Step 4: Paste the URL

Open `events/the-long-walk.html` and find this line near the bottom:

```javascript
var GOOGLE_SCRIPT_URL = 'YOUR_APPS_SCRIPT_URL';
```

Replace `YOUR_APPS_SCRIPT_URL` with the URL you copied. That's it.

## Testing

Open the event page, fill out the form, and check your Google Sheet. You should see a new row appear within a few seconds.
