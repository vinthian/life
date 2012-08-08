import pygame, sys
from pygame.locals import *
from life import *
from random import randint

class Game:
    def __init__(self, start=True):
        # Game/Display Settings
        self.width = 100
        self.height = 100
        self.pixel_size = 5

        # Pygame
        pygame.init()
        self.running = True
        self.paused = False
        self.color = 0
        self.speed = 30

        # Colors
        self.black_color = pygame.Color(0, 0, 0)
        self.white_color = pygame.Color(255, 255, 255)
        color_values = [280 - ((x + 1) * 25) for x in range(8)]
        gray_values = [55 + (x + 1) * 25 for x in range(8)]
        self.life_colors = [pygame.Color(x, 0, 0) for x in color_values]
        self.gray_colors = [pygame.Color(x, x, x) for x in gray_values]

        # Life
        self.life = Life(self.width, self.height)
        # Generate some patterns
        """
        for x in range(50):
            i = randint(0, 4)
            g = lambda a, b: (randint(0, a), randint(0, b))
            if i == 0:
                self.life._glider(*g(self.width - 3, self.height - 3))
            if i == 1:
                self.life._small_explorer(*g(self.width - 13, self.height - 13))
            if i == 2:
                self.life._osc1(*g(self.width - 3, self.height - 3))
            if i == 3:
                self.life._osc2(*g(self.width - 4, self.height - 4))
            if i == 4:
                self.life._osc3(*g(self.width - 4, self.height - 4))
        """
        self.life._gospers_glider_gun()

        # Init
        self.init_window()

        # Auto-start
        if start:
            self.main()

    def init_window(self):
        pygame.display.quit()
        pygame.display.init()
        self.fps_clock = pygame.time.Clock()
        self.game_window = pygame.display.set_mode(
            (self.width * self.pixel_size, self.height * self.pixel_size),
            pygame.RESIZABLE)

    def draw_cell(self, x, y, color):
        # Can't draw a 1x1 rectangle, so use Surface.set_at to draw 1x1 pixels
        if self.pixel_size == 1:
            self.game_window.set_at((x, y), color)
        else:
            self.game_window.fill(color,
                                  (x * self.pixel_size, y * self.pixel_size,
                                   self.pixel_size, self.pixel_size))

    def get_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.paused = False
            elif event.type == KEYDOWN:
                # Change speed, 0 = no speed restrictions
                if event.key == K_1:
                    if self.speed - 15 >= 0:
                        self.speed -= 15
                if event.key == K_2:
                    self.speed += 15
                # Change colors
                if event.key == K_3:
                    if self.color - 1 >= 0:
                        self.color -= 1
                        self.draw_update()
                if event.key == K_4:
                    if self.color + 1 <= 2:
                        self.color += 1
                        self.draw_update()
                # Change cell size
                if event.key == K_5:
                    if self.pixel_size - 1 > 0:
                        self.pixel_size -= 1
                        self.init_window()
                        self.draw_update()
                if event.key == K_6:
                    self.pixel_size += 1
                    self.init_window()
                    self.draw_update()
                # Pause
                if event.key == K_p:
                    self.paused = not self.paused
                # Next generation (only while paused)
                if event.key == K_SPACE:
                    if self.paused:
                        self.life.next()
                        self.draw_update()
                # Quit
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    def draw_update(self):
        # Update window title
        pygame.display.set_caption("gen: %s - fps: %s/%s - updates: %s" %
                                   (self.life.generation,
                                    round(self.fps_clock.get_fps()),
                                    self.speed,
                                    self.life.update_count))
        # Set background color
        self.game_window.fill(self.white_color)
        # Iterate through list of dirty cells and draw them
        for x, y in self.life.dirty_list:
            if self.life.grid[x, y] == 1:
                neighbors = lambda x, y: self.life.neighbor_count(x, y) - 1
                if self.color == 0:
                    self.draw_cell(x, y, self.life_colors[neighbors(x, y)])
                elif self.color == 1:
                    self.draw_cell(x, y, self.gray_colors[neighbors(x, y)])
                else:
                    self.draw_cell(x, y, self.black_color)
        # Draw
        pygame.display.update()

    def main(self):
        # Main Game Loop
        while self.running:
            self.draw_update()
            self.get_input()
            # Still get input while paused
            while self.paused:
                self.get_input()
            # Calculate next generation
            self.life.next()
            self.fps_clock.tick(self.speed)

        # Quit when game loop breaks
        pygame.quit()
        sys.exit()
