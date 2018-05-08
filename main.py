# Define some colors
import pygame
from pygame.locals import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()

# Set the width and height of the screen [width, height]

INITIAL_WIDTH, INITIAL_HEIGHT = 640, 480
scaleX, scaleY = 1, 1
width, height = INITIAL_WIDTH, INITIAL_HEIGHT

screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), HWSURFACE| DOUBLEBUF|RESIZABLE)
pygame.display.set_caption("Tikko Word Clock Emulator")

title_font = pygame.font.SysFont('Arial', 60)

done = False

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == VIDEORESIZE:
            width = event.dict['size'][0]
            height = event.dict['size'][1]
            scaleX = abs(width / INITIAL_WIDTH)
            scaleY = abs(height / INITIAL_HEIGHT)
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            pygame.display.flip()

    # render begin
    screen.fill(WHITE)

    # draw text
    title_text = title_font.render("Tikko Word Clock", True, (0, 0, 0))
    screen.blit(title_text, (width/2 - title_text.get_rect().width/2, 10))

    MATRIX_ROWS = 12
    MATRIX_COLUMNS = 12
    SPACING = 6;
    square_size = 20

    offset = 50
    squares = dict()

    for row in range(MATRIX_ROWS):
        for column in range(MATRIX_COLUMNS):
            index = row + MATRIX_COLUMNS * column
            x, y = SPACING * row, SPACING * column
            #squares[row + MATRIX_COLUMNS * column] = square = plt.Rectangle((x, y), square_size, square_size, fc='g')

            pygame.draw.rect(screen, (0, 0, 0), (offset + SPACING * x, offset + SPACING * y, square_size, square_size))

    pygame.display.flip()
    # render end
    clock.tick(144)

# Close the window and quit.
pygame.quit()