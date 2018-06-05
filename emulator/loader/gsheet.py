from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from .loader import MatrixLoader


class GSheetLoader(MatrixLoader):

    def load_matrix_values(self, emulator):
        letter_indices = dict()
        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', scopes)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        result = service.spreadsheets().values().get(spreadsheetId=emulator.args.spreadsheet_id,
                                                     range=emulator.args.layout_range).execute()

        values = result.get('values', [])
        emulator.log.info("Spreadsheet Layout retrieved.")
        for row in range(emulator.matrix_row_count):
            for column in range(emulator.matrix_column_count):
                letter = ""
                try:
                    letter = values[column][row]
                except IndexError:
                    pass
                letter_indices[row + emulator.matrix_column_count * column] = letter
        return letter_indices


    def load_word_states(self, emulator):
        words = dict()
        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', scopes)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        result = service.spreadsheets().values().get(spreadsheetId=emulator.args.spreadsheet_id,
                                                     range=emulator.args.words_range).execute()

        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            emulator.log.debug('Row, Word, Range:')
            for row in values:
                if len(row) >= 3:
                    emulator.log.debug("{}".format(row))

                # Print columns A and E, which correspond to indices 0 and 4.
        emulator.log.info("Spreadsheet Words retrieved.")

