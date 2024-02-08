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


class PinBall:
    s_width = 600
    s_height = 800
    color_black = (0, 0, 0)
    dt = 0.3  # timestep
    GRAVITY_X = 0.0  # Gravity in x direction
    GRAVITY_Y = 0.3  # Gravity in y direction
    loss = 0.12
    max_speed = 40
    ball_radius = 15
    starting_life = 3
    starting_money = 100
    starting_launch_speed = 0
    starting_trigger = False
    starting_last_launch = -10000

    def __init__(self):
        self.running = True
        self.dt = PinBall.dt
        self.loss = PinBall.loss
        self.max_speed = PinBall.max_speed
        self.ball_radius = PinBall.ball_radius
        self.gravity = Vector(PinBall.GRAVITY_X, PinBall.GRAVITY_Y)
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((PinBall.s_width, PinBall.s_height), pygame.RESIZABLE)
        bg_orig = pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
        score_tracker = ScoreTracker(screen)
        highscore_tracker = HighscoreTracker(screen, score_tracker)
        player = Player(PinBall.starting_life, screen)
        launcher = Launcher(score_tracker, PinBall.starting_money, PinBall.starting_launch_speed,
                            PinBall.starting_trigger, PinBall.starting_trigger)
        game_map = GameMap(self.ball_radius, screen, score_tracker)
        game_map.initialize_map()
        time = 0
        clock_tick = 120

        # Main event loop
        while self.running:
            # Adjust screen
            s_width, s_height = screen.get_width(), screen.get_height()
            bg = pygame.transform.scale(bg_orig, (s_width, s_height))
            screen.blit(bg, (0, 0))  # redraws background image

            for i in Ball.Balls:
                i.update(screen, self.dt, self.gravity, self.loss, self.max_speed, launcher, player)

            for i in Polygon.Polygons:
                i.update(screen, self.dt)

            launcher.launch(self.ball_radius, time, screen, clock_tick, self.max_speed)

            time += 1
            score_tracker.show()
            player.show()
            pygame.display.flip()  # Update the display of the full screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.initialize_exit(screen, highscore_tracker)

            if player.is_not_alive() or (len(Ball.Balls) <= 1 and launcher.current_money < 100):
                self.initialize_exit(screen, highscore_tracker)
            self.clock.tick(clock_tick)  # 120 frames per second
        pygame.quit()

    def initialize_exit(self, screen, highscore_tracker):
        highscore_tracker.update()
        screen.fill(PinBall.color_black)
        highscore_tracker.render_multi_line()
        pygame.display.flip()
        sleep(5)
        self.running = False
