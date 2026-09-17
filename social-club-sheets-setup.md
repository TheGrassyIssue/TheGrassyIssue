# Social Club sign-ups → Google Sheet

**Status: live as of 17 Sept 2026.** The endpoint is deployed, pasted into
`events/social-club.html` and into `build-social-club.py`, and verified reachable
and public. Steps 1–4 below are done; they are kept as a record of how it was set
up and what to do if it ever needs redeploying. **Step 5 is still yours** — send
one real test sign-up and confirm the row lands.

This is a **separate sheet and script from The Long Walk**, on purpose, so the two
interest lists stay apart.

---

## 1. Make the sheet

1. New Google Sheet. Call it **TGI Social Club — Interest List**.
2. In row 1, put these five headers, in this order, spelled exactly:

```
Timestamp   Name   Email   Range   Mode
```

---

## 2. Add the script

In that sheet: **Extensions → Apps Script**. Delete whatever is in the editor and
paste this in:

```javascript
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var data  = JSON.parse(e.postData.contents);
  sheet.appendRow([
    data.timestamp || new Date().toISOString(),
    data.name  || '',
    data.email || '',
    data.range || '',
    data.mode  || ''
  ]);
  return ContentService
    .createTextOutput(JSON.stringify({ result: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

Save it (the disk icon). Name the project **TGI Social Club** when it asks.

---

## 3. Deploy it

1. **Deploy → New deployment**.
2. Click the gear next to "Select type" and choose **Web app**.
3. Set:
   - **Execute as:** Me
   - **Who has access:** **Anyone** ← this one matters. "Anyone with Google
     account" will silently reject submissions from logged-out visitors, which is
     most of them.
4. **Deploy**. Google will ask you to authorize — it warns that the app is
   unverified because you wrote it yourself. Advanced → Go to TGI Social Club.
5. Copy the **Web app URL**. It looks like
   `https://script.google.com/macros/s/AKfycb…/exec`.

---

## 4. Paste the URL into the page  ✅ done

Done in both places — `events/social-club.html` and `build-social-club.py`. Both
had to change: the builder regenerates the page, so a URL set only in the HTML
would be wiped the next time the page was rebuilt.

A build-time guard now refuses to write the page if it ever points at The Long
Walk's script, or at a `/dev` URL instead of `/exec`.

Verified on 17 Sept 2026: a plain GET to the endpoint returns *"Script function
not found: doGet"*. That is the correct answer — it proves the URL resolves and
that access is set to **Anyone** (a login wall would have redirected instead),
and it confirms only `doPost` is defined, which is what the form uses.

---

## 5. Test it  ← still to do

Load `/events/social-club`, fill the form in with your own name, submit. A row
should appear in the sheet within a couple of seconds.

If nothing shows up:

- **Most likely:** access is set to "Anyone with Google account" rather than
  "Anyone". Redeploy with the right setting.
- The form posts with `mode: 'no-cors'`, so the browser cannot read the response
  and the page will show the success panel either way. The sheet is the only
  place to confirm it actually worked — always check there when testing.
- Editing the script later needs **Deploy → Manage deployments → edit → New
  version**, or your change will not go live.

---

## What gets collected

| Column | From | Values |
|---|---|---|
| Timestamp | automatic | ISO 8601 |
| Name | text field | free text |
| Email | email field | validated by the browser |
| Range | dropdown | `austin-only`, `45`, `90`, `anywhere` |
| Mode | dropdown | `walk`, `ride`, `either` |

Range and Mode are optional, so both can come through empty. They are the two
answers that decide which group someone fits into, which is why they are the only
questions beyond name and email — every extra field costs sign-ups.

The form also posts `source: 'social-club'`. The script above ignores it, but it
is there if you ever do merge the two lists into one sheet and need to tell them
apart.
