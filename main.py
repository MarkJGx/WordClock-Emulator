#!/usr/bin/python3

from __future__ import print_function
import matplotlib.pyplot as plt
from random import randint

import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('commandgoeshere', type=str)
# Tikko Word Clock Matrix
MATRIX_ROWS = 12
MATRIX_COLUMNS = 12
SPACING = 1.25;
plt.axes()

squares = dict()

for row in range(MATRIX_ROWS):
    for column in range(MATRIX_COLUMNS):
        square_size = 1
        index = row + MATRIX_COLUMNS * column
        x,y = SPACING * row, SPACING * column
        squares[row + MATRIX_COLUMNS * column] = square = plt.Rectangle((x,y), square_size, square_size, fc='g')
        plt.gca().add_patch(square)
        plt.text(0.15+x, 0.125+y, '1', fontsize=16)

fig = plt.gcf()
fig.canvas.set_window_title('Tikko Word Clock Emulator')


plt.axis('scaled')


plt.show()


