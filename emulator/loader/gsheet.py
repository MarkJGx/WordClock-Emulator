from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from .loader import MatrixLoader


class GSheetLoader(MatrixLoader):

    def load_matrix_values(self, emulator):
        led_indices = dict()
        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', scopes)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        result = service.spreadsheets().values().get(spreadsheetId=emulator.args.spreadsheet_id,
                                                     range=emulator.args.range_name).execute()

        values = result.get('values', [])
        emulator.log.info("Spreadsheet retrieved.")
        for row in range(emulator.matrix_row_count):
            for column in range(emulator.matrix_column_count):
                letter = ""
                try:
                    letter = values[column][row]
                except IndexError:
                    pass
                led_indices[row + emulator.matrix_column_count * column] = letter
        return led_indices
