import pygame, sys
from pygame.locals import *

from life import *

from random import randint

# Game/Display Settings
width = 50
height = 50
pixel_size = 5

# Pygame
pygame.init()
pygame.display.init()
fps_clock = pygame.time.Clock()

game_window = pygame.display.set_mode((width * pixel_size, height * pixel_size))

black_color = pygame.Color(0, 0, 0)
white_color = pygame.Color(255, 255, 255)

color_values = [(x + 1) * 31 for x in range(8)]
life_colors = [pygame.Color(x, x, x) for x in color_values]

def draw_pixel(x, y, color):
    pygame.draw.rect(game_window, color,
                     (x * pixel_size, y * pixel_size,
                      pixel_size, pixel_size))

# Life
life = Life(width, height)
life._glider(10, 10)
life._small_explorer(30, 10)

running = True
while running:
    pygame.display.set_caption("Life - gen: %s - fps: %s" %
                               (life.generation, round(fps_clock.get_fps())))
    game_window.fill(white_color)
    
    for y in range(life.grid.height):
        for x in range(life.grid.width):
            if life.grid[x, y] == 1:
                draw_pixel(x, y, life_colors[life.neighbor_count(x, y) - 1])

    life.next()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    pygame.display.update()
    fps_clock.tick(30)

pygame.quit()
sys.exit()
