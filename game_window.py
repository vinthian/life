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
        pygame.display.init()
        self.fps_clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.color = 0
        self.speed = 30

        self.game_window = pygame.display.set_mode(
            (self.width * self.pixel_size, self.height * self.pixel_size))

        self.black_color = pygame.Color(0, 0, 0)
        self.white_color = pygame.Color(255, 255, 255)

        color_values = [280 - ((x + 1) * 25) for x in range(8)]
        gray_values = [55 + (x + 1) * 25 for x in range(8)]
        self.life_colors = [pygame.Color(x, 0, 0) for x in color_values]
        self.gray_colors = [pygame.Color(x, x, x) for x in gray_values]

        # Life
        self.life = Life(self.width, self.height)
        self.life._gospers_glider_gun()
        """
        for x in range(5):
        life._glider(randint(0, width - 3), randint(0, height - 3))
        life._small_explorer(randint(0, width - 13), randint(0, height - 13))
        """

        # Auto-start
        if start:
            self.main()

    def draw_pixel(self, x, y, color):
        pygame.draw.rect(self.game_window, color,
                         (x * self.pixel_size, y * self.pixel_size,
                          self.pixel_size, self.pixel_size))

    def key_helper(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                self.paused = False
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    if self.speed - 15 > 0:
                        self.speed -= 15
                if event.key == K_2:
                    self.speed += 15
                if event.key == K_3:
                    if self.color - 1 >= 0:
                        self.color -= 1
                        self.draw_update()
                if event.key == K_4:
                    if self.color + 1 <= 2:
                        self.color += 1
                        self.draw_update()
                if event.key == K_p:
                    self.paused = not self.paused
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    def draw_update(self):
        self.game_window.fill(self.white_color)
        for x, y in self.life.dirty_list:
            if self.life.grid[x, y] == 1:
                if self.color == 0:
                    self.draw_pixel(
                        x, y,
                        self.life_colors[self.life.neighbor_count(x, y) - 1])
                elif self.color == 1:
                    self.draw_pixel(
                        x, y,
                        self.gray_colors[self.life.neighbor_count(x, y) - 1])
                else:
                    self.draw_pixel(x, y, self.black_color)
        pygame.display.update()

    def main(self):
        # Main Game Loop
        while self.running:
            pygame.display.set_caption("gen: %s - fps: %s/%s - updates: %s" %
                                       (self.life.generation,
                                        round(self.fps_clock.get_fps()),
                                        self.speed,
                                        self.life.update_count))
            self.draw_update()
            self.key_helper()

            while self.paused:
                self.key_helper()

            self.life.next()
            self.fps_clock.tick(self.speed)

        # Quit
        pygame.quit()
        sys.exit()
