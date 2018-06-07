class WordRange:
    def __init__(self, row: int, min_x: int, max_x: int):
        self.row = row
        self.min_x = min_x
        self.max_x = max_x

    def __repr__(self):
        return "WordRange(row: {}, min_x: {}, max_x {})".format(self.row, self.min_x, self.max_x)


class WordState:
    def __init__(self, word: str, word_ranges: tuple):
        self.word = word
        self.word_ranges = word_ranges

    def __repr__(self):
        return "WordState(word: {}, word_ranges: {})".format(self.word, self.word_ranges)

class LED:
    def __init__(self, on=False, color=(0, 0, 0), letter=""):
        self.on = on
        self.color = color
        self.letter = letter