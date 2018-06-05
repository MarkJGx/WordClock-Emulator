# TODO QoL  - add proper debugging
# TODO perf -  add threaded asyincio
# TODO code - replace led_indices with list
import pygame
import random
import logging
import sys
import argparse
from emulator.render import Render
from emulator.loader.gsheet import GSheetLoader
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from pygame.locals import *
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class WordState:
    def __init__(self, word, row, min, max):
        self.word = word
        self.row = row
        self.min = min
        self.max = max


class LED:
    def __init__(self, on=False, color=(0, 0, 0), letter=""):
        self.on = on
        self.color = color
        self.letter = letter


class Emulator:
    __slots__ = ('args', 'log', 'led_indices', 'render', 'matrix_loader', 'words')

    def __init__(self, args, log):
        self.args = args
        self.log = log
        self.led_indices = dict()
        self.render = Render()
        self.matrix_loader = GSheetLoader()

    IR = WordState("IR", 0, 0, 2)
    PIECI = WordState("PIECI", 1, 0, 5)
    VIENS = WordState("VIENS", 3, 0, 5)


    def run(self):
        self.load_leds()
        self.matrix_loader.load_word_states(self)
        while True:
            active_words = [Emulator.IR, Emulator.PIECI, Emulator.VIENS]
            for active_word in active_words:
                start_index = active_word.min + self.matrix_column_count * active_word.row
                for range_index in range(active_word.min, active_word.max):
                    self.led_indices[start_index + range_index].on = True
            if self.render.draw(self):
                break
        self.render.quit()

    def load_leds(self):
        letter_indices = self.matrix_loader.load_matrix_values(self)
        for index, letter in letter_indices.items():
            self.led_indices[index] = LED(on=False, color=(255, 50, 0), letter=letter)

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
