import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from pytz import timezone

class sheetsWrapper:
    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        self.scope = ['https://www.googleapis.com/auth/drive.appdata', 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/drive.file']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.login()


    def updateIndex(self):
        rowIdx = self.worksheet.acell('G2').value

        self.row = int(rowIdx) + 1
        self.worksheet.update_acell('G2', self.row)

    def updateLog(self, State, Device):
        self.updateIndex()
        range_build = 'A' + str(self.row) + ':D' + str(self.row)
        cell_list = self.worksheet.range(range_build)

        Arizona = timezone('US/Arizona')
        dateNow = str(datetime.date.today())
    #    timeNow = str(datetime.datetime.now(Arizona))
        timeNow = str(datetime.datetime.time(datetime.datetime.now(Arizona)).replace(microsecond=0))
        cell_values = [dateNow, timeNow, State, Device]
        print(cell_values)

        for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
            cell_list[i].value = val  # use the index on cell_list and the val from cell_values

        self.worksheet.update_cells(cell_list)

    def login(self):
        self.client = gspread.authorize(self.creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        try:
            self.sheet = self.client.open_by_url("https://docs.google.com/spreadsheets/d/18X1VU-dwj_tOA4V95_a1Tv6q7zXABOPRV5i5_l0T8kc/edit#gid=0")
            print('Opened sheet')
        except:
            self.client.create("UnlockLog")
            print("made a new one")
            self.sheet = self.client.open("UnlockLog").sheet1
        self.worksheet = self.sheet.get_worksheet(0)
        self.row = 1