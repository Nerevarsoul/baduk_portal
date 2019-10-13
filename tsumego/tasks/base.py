import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class BaseSpreadSheetParser:
    # SPREADSHEET_ID = '1sCWQkWw0K8I77CWrmLeLHwiSCNnBV4HBXg2NMJ7gT9Y'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()

    def get_all_ranges(self):
        result = self.sheet.get(spreadsheetId=self.spreadsheet_id).execute()
        return [sheet['properties']['title'] for sheet in result.get('sheets')]

    @property
    def creds(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def get_sheet(self, sheet):
        return self.sheet.values.get(spreadsheetId=self.spreadsheet_id, range=sheet)
