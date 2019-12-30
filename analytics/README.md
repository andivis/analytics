# analytics

## Installation

1. Make sure you have Python version 3.8 or higher installed
2. Run the command below in a command prompt. Or if you're on Windows, just run the file called `run-windows.bat`.

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Instructions

1. Create or open a Google Sheet.
2. Put your list of url's in column A. One url per row.
3. Copy the spreadsheet id from the url in your browser. It's the part between `/d/` and `/edit` Paste it into `options.ini`. The file must look like `spreadSheetId=your spreadsheet id`
4. Open a command prompt and run `python analytics.py`
5. It will open a browser to connect to your Google account. It will complain that the app may be unsafe. Click allow.
6. There may be a long pause. Then the script should finish.
7. Go to the sheet and you'll see the regex in column B.