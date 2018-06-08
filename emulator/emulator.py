# TODO QoL  - add proper debugging
# TODO perf -  add threaded asyincio
# TODO code - replace led_indices with list
from emulator import LED
from emulator.render import Render
from emulator.loader.gsheet import GSheetLoader
import datetime
import random
import threading
import pygame
import time

class Emulator:
    __slots__ = ('args', 'log', 'led_indices', 'render', 'matrix_loader', 'words', 'clock', 'timings', 'word_states')

    def __init__(self, args, log):
        self.args = args
        self.log = log
        self.led_indices = dict()
        self.render = Render()
        self.matrix_loader = GSheetLoader()
        self.timings = dict()
        self.word_states = dict()


#    IR = WordState("IR", 0, 0, 2)
 #   PIECI = WordState("PIECI", 1, 0, 5)
  #  VIENS = WordState("VIENS", 3, 0, 5)

    def update(self):
        self.load_leds()
        self.timings = self.matrix_loader.load_timings(self)
        self.word_states = self.matrix_loader.load_word_states(self)
        self.log.debug("Refresh.")
       # threading.Timer(5.0, self.update).start()

    def run(self):
        active_words = list()
        color = (random.randint(125, 255), random.randint(125, 255), random.randint(125, 255))
        self.update()
        while True:
            # TODO fix crashing with timings
            now = datetime.datetime.now()

            actual_hour = abs(now.hour - 12)
            self.log.debug("before: {}".format(actual_hour))

            current_hours = self.timings[actual_hour]
            self.log.debug(actual_hour)
            active_words.clear()
            for hour in current_hours:
                if hour in self.word_states:
                    active_words.append(self.word_states[hour])

            #self.log.debug("current hour {}".format(current_hours))
            for active_word in active_words:
                for word_range in active_word.word_ranges:
                    start_index = word_range.min_x + self.matrix_column_count * word_range.row
                    for range_index in range(0, word_range.max_x - word_range.min_x):
                        self.led_indices[start_index + range_index].on = True
                        self.led_indices[start_index + range_index].color = color

            if self.render.draw(self):
                break
            self.flip_leds()

        self.render.quit()

    def flip_leds(self):
        for index, led in self.led_indices.items():
            led.on = False

    def load_leds(self):
        letter_indices = self.matrix_loader.load_matrix_values(self)
        for index, letter in letter_indices.items():
            self.led_indices[index] = LED(on=True, color=(255, 50, 0), letter=letter)

    _off_color = (50, 50, 50)
    _matrix_column_count = 12
    _matrix_row_count = 12


    @property
    def off_color(self):
        return type(self)._off_color

    @property
    def matrix_row_count(self):
        return type(self)._matrix_row_count

    @property
    def matrix_column_count(self):
        return type(self)._matrix_column_count
