import pickle
import os.path
import re
import helpers
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def getAfterDomain(url):
    result = helpers.findBetween(url, '//', '')
    result = helpers.findBetween(result, '/', '')

    if len(url) > 0 and url[-1] == '/':
        result = result[:-1]

    return result

def main():
    print('Starting')

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If modifying these scopes, delete the file token.pickle.
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    spreadsheetId = helpers.getFile('options.ini')
    spreadsheetId = helpers.findBetween(spreadsheetId, '=', '')

    if not spreadsheetId:
        while not spreadsheetId:
            spreadsheetId = input('Paste your spreadsheet id here: ')
    
    print('Getting spreadsheet')
    
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    try:
        result = sheet.values().get(spreadsheetId=spreadsheetId, range='A:A').execute()
        values = result.get('values', [])
    except:
        print('Error: could not get the spreadsheet. Stopping.')
        exit()

    valuesToUpdate = []

    if not values:
        print('No data found.')
        exit()

    currentRow = ''

    i = 0

    maximumRegexLength = 7000

    for row in values:
        if not row:
            i += 1
            continue

        print('On row %d: %s' % (i, row[0]))

        partAfterDomain = getAfterDomain(row[0])
        regex = re.escape(partAfterDomain)

        if len(regex) >= maximumRegexLength:
            print('Skipping. Regex is too long for this url.')
            i += 1
            continue

        #reached length limit?
        if row[0] and len(currentRow) + len(regex) >= maximumRegexLength:
            #remove extra character if needed
            if currentRow and currentRow[-1] == '|' and currentRow[-2:-1] != '\|':
                currentRow = currentRow[:-1]
                
            #end this row
            print('\nWill send this regex: ' + currentRow + '\n')

            newRow = [currentRow]
            valuesToUpdate.append(newRow)
            
            #start a new row
            currentRow = regex

        elif row:
            #add to current row
            currentRow += regex;

        if row[0] and i < len(values) - 1:
            currentRow += '|'

        i += 1

    if currentRow:
        #remove extra character if needed
        if currentRow[-1] == '|' and currentRow[-2:-1] != '\|':
            currentRow = currentRow[:-1]

        print('\nWill send this regex: ' + currentRow + '\n')        

        newRow = [currentRow]
        valuesToUpdate.append(newRow)

    Body = {
        'values' : valuesToUpdate,
    }

    result = 'success'
    
    try:
        result = sheet.values().update(spreadsheetId=spreadsheetId, range='B:B', valueInputOption='RAW', body=Body).execute()
        print('Updated the spreadsheet successfully')
        print('Done')
    except Exception as e:
        print('')
        print(e)
        print('')
        print('Something went wrong when trying to update the spreadsheet')
        print('Exiting')
        
    input("Press Enter to continue...")

if __name__ == '__main__':
    main()