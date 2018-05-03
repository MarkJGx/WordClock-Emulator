#!/usr/bin/python3

from __future__ import print_function
import matplotlib.pyplot as plt
from random import randint

import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('commandgoeshere', type=str)

MATRIX_ROWS = 12
MATRIX_COLUMNS = 12
SPACING = 1.25;
plt.axes()

squares = dict()

for row in range(MATRIX_ROWS):
    for column in range(MATRIX_COLUMNS):
        squares[row + MATRIX_COLUMNS * column] = square = plt.Rectangle((SPACING * row, SPACING * column), 1, 1, fc='g')
        plt.gca().add_patch(square)

plt.axis('scaled')
plt.show()


