from .loader import MatrixLoader
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from emulator import WordState, WordRange

class GSheetLoader(MatrixLoader):


    def get_sheet(self, emulator):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('secret_service_key.json', scope)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(emulator.args.spreadsheet_id)
        return sheet

    def load_matrix_values(self, emulator):
        letter_indices = dict()
        sheet = self.get_sheet(emulator)
        layout_sheet = sheet.worksheet(emulator.args.layout_sheet)
        cell_list = layout_sheet.range(emulator.args.layout_range)

        for cell in cell_list:
            letter_indices[(cell.col - 1) + emulator.matrix_column_count * (cell.row - 1)] = cell.value
        emulator.log.info("Spreadsheet Layout retrieved.")
        return letter_indices

    def load_word_states(self, emulator):
        sheet = self.get_sheet(emulator)
        words_sheet = sheet.worksheet(emulator.args.words_sheet)
        cell_list = words_sheet.range(emulator.args.words_range)

        word_states = list()
        for i in range(0, len(cell_list), 2):
            word_name = cell_list[i].value
            word_ranges = self.notation_to_word_ranges(cell_list[i + 1].value, emulator)
            if word_ranges:
                word_states.append(WordState(word_name, word_ranges))

        emulator.log.debug(word_states)
        emulator.log.info("Spreadsheet Words retrieved.")
        return word_states

    # tuple: row, min_x, max_y


    def notation_to_word_ranges(self, given_notation, emulator) -> tuple:
        if given_notation:
            notations = given_notation.split(",")
            word_ranges = tuple()
            for notation in notations:
                if notation is not None:
                    notation = notation.replace(emulator.args.layout_sheet + '!','')
                    notation_ranges = notation.split(":")
                    if len(notation_ranges) == 2:
                        xy_start = gspread.utils.a1_to_rowcol(notation_ranges[0])
                        xy_end = gspread.utils.a1_to_rowcol(notation_ranges[1])
                        same_row = xy_start[0] == xy_end[0]
                        if same_row:
                            min_x = xy_start[1]
                            max_x = xy_end[1]
                            word_ranges = word_ranges + (WordRange(xy_start[0] - 1, min_x - 1, max_x),)
                        else:
                            start_row, end_row = xy_start[0] - 1, xy_end[0]
                            diff = abs(end_row - start_row)
                            for i in range(0, diff):
                                min_x = xy_start[1]
                                max_x = xy_end[1]
                                word_ranges = word_ranges + (WordRange(start_row + i, min_x - 1, max_x),)

                    else:
                        pass
            return word_ranges
        else:
            return None