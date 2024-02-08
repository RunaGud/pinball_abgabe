import math
from pathlib import Path
import pygame
from time import sleep

from Ball import Ball
from GameMap import GameMap
from HighscoreTracker import HighscoreTracker
from Launcher import Launcher
from Player import Player
from Polygon import Polygon
from ScoreTracker import ScoreTracker
from Vector import Vector

pygame.init()

# Initial window size
s_width = 600
s_height = 800
color_black = (0, 0, 0)

pygame.RESIZABLE = False

# Making display screen
screen = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()

# Setup
running = True

GRAVITY_X = 0.0  # Gravity in x direction
GRAVITY_Y = 0.3  # Gravity in y direction
dt = 0.3  # timestep
loss = 0.12
max_speed = 40
down = 15
ball_radius = 15
gravity = Vector(GRAVITY_X, GRAVITY_Y)
clock = pygame.time.Clock()
score_tracker = ScoreTracker(screen)
highscore_tracker = HighscoreTracker(screen, score_tracker)
player = Player(3, screen)
launcher = Launcher(score_tracker, 100, 0, False, -20000)
game_map = GameMap(ball_radius, screen, score_tracker)

# creating balls
b6 = Ball(Vector(300, 150),
          Vector(0, 0),
          ball_radius * 2,
          20,
          [0, 255, 255],
          score_tracker,
          False)

floating_square = Polygon([Vector(30 + ball_radius * 0.1, 300), Vector(80 + ball_radius * 0.1, 300),
                           Vector(80 + ball_radius * 0.1, 200), Vector(30 + ball_radius * 0.1, 200)],
                          Vector(55, 250),
                          Vector(0, 0),
                          [200, 200, 250],
                          score_tracker,
                          0.0,
                          0.05,
                          True)

# Initializing map
game_map.initialize_map()

start_pos = Vector(s_width - (ball_radius * 1.3), s_height * 0.7)

time = 0
clock_tick = 120

# Main event loop
while running:
    # Adjust screen        
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0))  # redraws background image

    for i in Ball.Balls:
        i.update(screen, dt, gravity, loss, max_speed, launcher, player)

    for i in Polygon.Polygons:
        i.update(screen, dt)

    Launcher.launch(launcher, start_pos, ball_radius, time, screen, clock_tick, max_speed)

    # constantly moving objects
    b6.speed.x = 50 * 0.06 * math.cos(0.03 * time)
    floating_square.speed.y = 5 * math.sin(0.01 * time)

    time += 1
    score_tracker.show()
    player.show()
    pygame.display.flip()  # Update the display of the full screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                highscore_tracker.update()
                screen.fill(color_black)
                highscore_tracker.render_multi_line()
                pygame.display.flip()
                sleep(5)
                running = False

    if player.is_not_alive() or (len(Ball.Balls) <= 1 and launcher.current_money < 100):
        highscore_tracker.update()
        screen.fill(color_black)
        highscore_tracker.render_multi_line()
        pygame.display.flip()
        sleep(5)
        running = False
    clock.tick(clock_tick)  # 120 frames per second
