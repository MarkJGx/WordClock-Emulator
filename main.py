# TODO QoL - add proper debugging
# TODO QoL -cleanup code
# TODO QoL - move rendering and logic to their own classes
# TODO performance - multi thread google sheets
import pygame
import random
import logging
import sys
import argparse
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from pygame.locals import *
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

log = logging.getLogger('WordClock')
formatter = logging.Formatter('%(threadName)s:[%(levelname)s] %(message)s')

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(logging.DEBUG)

log.info('Running.')

# usage ./generate_layout.py "sheet_id" "range_name"
parser = argparse.ArgumentParser()
parser.add_argument('spreadsheet_id', type=str)
parser.add_argument('range_name', type=str)


args = parser.parse_args()
class LED:
    def __init__(self, on=False, color=(0, 0, 0), letter=""):
        self.on = on
        self.color = color
        self.letter = letter


matrix_rows = 12
matrix_columns = 12

led_indicies = dict()

OFF_COLOR = (50, 50, 50)


def load_leds():
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    result = service.spreadsheets().values().get(spreadsheetId=args.spreadsheet_id,
                                                 range=args.range_name).execute()

    values = result.get('values', [])
    for row in range(matrix_rows):
        for column in range(matrix_columns):
            letter = ""
            try:
                letter = values[column][row]
                # print("{}, {}: value {}".format(row, column, values[row][column]))
            except IndexError:
                pass
            led_indicies[row + matrix_columns * column] = LED(on=random.randint(0, 1) == 0, letter=letter,
                                                              color=(255, 125, 125))
    log.info("Loaded LED(s) from spreadsheet.")


# https://stackoverflow.com/questions/28492103/how-to-combine-python-asyncio-with-threads?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
load_leds()

pygame.init()
clock = pygame.time.Clock()

# Set the width and height of the screen [width, height]

INITIAL_WIDTH, INITIAL_HEIGHT = 640, 480
scale_x, scale_y, scale_mul = 1, 1, 1
width, height = INITIAL_WIDTH, INITIAL_HEIGHT

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Tikko Word Clock Emulator")

title_font = pygame.font.SysFont('Arial', 42)

INITAL_LETTER_FONT_SIZE = 32

letter_font = pygame.font.SysFont('Arial', INITAL_LETTER_FONT_SIZE)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == VIDEORESIZE:
            width = event.dict['size'][0]
            height = event.dict['size'][1]
            scale_x = abs(width / INITIAL_WIDTH)
            scale_y = abs(height / INITIAL_HEIGHT)
            scale_mul = (scale_x + scale_y) / 2
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

            letter_font = pygame.font.SysFont('Arial', int(round(INITAL_LETTER_FONT_SIZE * scale_mul)))

            pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            load_leds()
    # render begin
    screen.fill(BLACK)

    # draw text
    # title_text = title_font.render("Tikko Word Clock", True, (0, 0, 0))
    # screen.blit(title_text, (width / 2 - title_text.get_rect().width / 2, 2))
    spacing = 6;
    square_size = 20 * scale_mul
    matrix_width = ((spacing * (matrix_rows - 1)) * scale_mul) * spacing + square_size
    matrix_height = ((spacing * (matrix_columns - 1)) * scale_mul) * spacing + square_size

    offset_y = height / 2 - matrix_height / 2
    offset_x = width / 2 - matrix_width / 2
    for row in range(matrix_rows):
        for column in range(matrix_columns):
            led = led_indicies[row + matrix_columns * column]
            x, y = (spacing * spacing * row) * scale_mul + offset_x, (spacing * spacing * column) * scale_mul + offset_y
            pygame.draw.rect(screen, led.on and led.color or OFF_COLOR, (x, y, square_size, square_size))
            if led.on:
                letter_text = letter_font.render(led.letter, True, (0, 0, 0))
                screen.blit(letter_text, (x + square_size / 2 - letter_text.get_rect().width / 2,
                                          y + square_size / 2 - letter_text.get_rect().height / 2 + 3))

    # pygame.draw.rect(screen, (0, 255, 1), (0, 0, square_size, matrix_height))
    # print("scale x: {}, scale y: {}, scale mul: {}".format(scale_x, scale_y, scale_mul))

    pygame.display.flip()
    # render end
    clock.tick(144)

# Close the window and quit.
pygame.quit()
