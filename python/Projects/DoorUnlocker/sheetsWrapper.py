import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

class sheetsWrapper:
    def __init__(self):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://www.googleapis.com/auth/drive.appdata', 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/drive.file']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open("UnlockLog").sheet1
        self.row = 1


    def updateIndex(self):
        rowIdx = self.sheet.acell('G2').value
        self.row = int(rowIdx) + 1
        self.sheet.update_acell('G2', self.row)

    def updateLog(self):
        self.updateIndex()
        range_build = 'A' + str(self.row) + ':D' + str(self.row)
        cell_list = self.sheet.range(range_build)

        dateNow = str(datetime.date.today())
        timeNow = str(datetime.datetime.time(datetime.datetime.now()).replace(microsecond=0))
        cell_values = [dateNow, timeNow, 'open', 'Pixel']
        print(cell_values)

        for i, val in enumerate(cell_values):  # gives us a tuple of an index and value
            cell_list[i].value = val  # use the index on cell_list and the val from cell_values

        self.sheet.update_cells(cell_list)