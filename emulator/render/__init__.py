# from emulator import Emulator
import pygame
from pygame.locals import *


class Render:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tikko Word Clock Emulator")
        self.width, self.height = self.default_width, self.default_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.default_width, self.default_height),
                                              HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.scale_x, self.scale_y, self.scale_mul = 1, 1, 1
        self.letter_font = pygame.font.SysFont('Arial', int(round(self.default_font_size * self.scale_mul)))

    _render_tick_rate = 60
    _default_width, _default_height = 640, 480
    _default_font_size = 32

    @property
    def default_font_size(self):
        return type(self)._default_font_size

    @property
    def default_width(self):
        return type(self)._default_width

    @property
    def default_height(self):
        return type(self)._default_height

    @property
    def render_tick_rate(self):
        return type(self)._render_tick_rate

    def draw(self, emulator):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == VIDEORESIZE:
                self.width, self.height = event.dict['size'][0], event.dict['size'][1]
                self.scale_x, self.scale_y = abs(self.width / self.default_width), abs(
                    self.height / self.default_height)
                self.scale_mul = (self.scale_x + self.scale_y) / 2
                self.screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

                self.letter_font = pygame.font.SysFont('Arial', int(round(self.default_font_size * self.scale_mul)))

                pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[K_r]:
                emulator.load_leds()

        self.screen.fill((0, 0, 0))

        spacing = 6;
        square_size = 20 * self.scale_mul
        matrix_width = ((spacing * (emulator.matrix_row_count - 1)) * self.scale_mul) * spacing + square_size
        matrix_height = ((spacing * (emulator.matrix_column_count - 1)) * self.scale_mul) * spacing + square_size

        offset_x, offset_y = self.width / 2 - matrix_width / 2, self.height / 2 - matrix_height / 2
        if emulator.led_indices:
            for row in range(emulator.matrix_row_count):
                for column in range(emulator.matrix_column_count):
                    led = emulator.led_indices[row + emulator.matrix_column_count * column]
                    x, y = (spacing * spacing * row) * self.scale_mul + offset_x, (
                            spacing * spacing * column) * self.scale_mul + offset_y
                    pygame.draw.rect(self.screen, led.on and led.color or emulator.off_color,
                                     (x, y, square_size, square_size))
                    if led.on:
                        letter_text = self.letter_font.render(led.letter, True, (0, 0, 0))
                        self.screen.blit(letter_text, (x + square_size / 2 - letter_text.get_rect().width / 2,
                                                       y + square_size / 2 - letter_text.get_rect().height / 2 + 3))
        pygame.display.flip()
        self.clock.tick(self.render_tick_rate)

    def quit(self):
        pygame.quit()
