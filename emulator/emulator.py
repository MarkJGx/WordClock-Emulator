# TODO QoL  - add proper debugging
# TODO perf -  add threaded asyincio
# TODO code - replace led_indices with list
from emulator import LED
from emulator.render import Render
from emulator.loader.gsheet import GSheetLoader
import random
import pygame
import time

class Emulator:
    __slots__ = ('args', 'log', 'led_indices', 'render', 'matrix_loader', 'words', 'clock')

    def __init__(self, args, log):
        self.args = args
        self.log = log
        self.led_indices = dict()
        self.render = Render()
        self.matrix_loader = GSheetLoader()


#    IR = WordState("IR", 0, 0, 2)
 #   PIECI = WordState("PIECI", 1, 0, 5)
  #  VIENS = WordState("VIENS", 3, 0, 5)


    def run(self):
        self.load_leds()
        word_states = self.matrix_loader.load_word_states(self)
        active_words = word_states
        current_milli_time = lambda: int(round(time.time() * 1000))
        refresh_time_ms = current_milli_time()
        while True:
            time_passed_ms = current_milli_time() - refresh_time_ms
            # if time_passed_ms >= 2000:
            #     active_words.clear()
            #     for amount in range(0, random.randint(0, 5)):
            #         active_words.append(word_states[random.randrange(len(word_states))])
            #     refresh_time_ms = current_milli_time()
            #     self.log.debug("Refreshed words.")
            # TODO bug BEZ refreshes at ranges 3, 6 instead of PUS
            if time_passed_ms >= 1000:
                self.flip_leds()
                word_states = self.matrix_loader.load_word_states(self)
                active_words = word_states
                for active_word in active_words:
                    for word_range in active_word.word_ranges:
                        start_index = word_range.min_x + self.matrix_column_count * word_range.row
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        for range_index in range(0, word_range.max_x - word_range.min_x):

                            self.led_indices[start_index + range_index].on = True
                            self.led_indices[start_index + range_index].color = color
                refresh_time_ms = current_milli_time()
            if self.render.draw(self):
                break

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
