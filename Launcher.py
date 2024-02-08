import math
import pygame
import random
from Vector import Vector

from Ball import Ball
import ScoreTracker


class Launcher:
    """
    A class that represents a ball launcher
    """
    default_cost = 100

    def __init__(self, score_tracker: ScoreTracker, current_money=100, launch_speed=-40, trigger=False,
                 last_launch=-20000):

        self.current_money = current_money
        self.launch_speed = launch_speed
        self.trigger = trigger
        self.score_tracker = score_tracker
        self.last_launch = last_launch
        self.launch_cost = Launcher.default_cost

    def _create_launch_strip_points(self, ball_radius, height, screen: pygame.Surface):
        s_width, s_height = screen.get_width(), screen.get_height()
        launch_stripe = [[s_width - ball_radius * 2.5, s_height * 0.76],
                         [s_width - ball_radius * 2.5,
                          s_height * 0.2 * (height / 100) + s_height * 0.76 * 0.01 * (100 - height)],
                         [s_width * 1 - ball_radius * 4,
                          s_height * 0.2 * (height / 100) + s_height * 0.76 * 0.01 * (100 - height)],
                         [s_width * 1 - ball_radius * 4, s_height * 0.76]]
        return launch_stripe

    def launch(self, ball_radius, time, screen, clock_tick, max_speed):
        start_pos = Vector(screen.get_width() - (ball_radius * 1.3), screen.get_height() * 0.7)
        height_money = min(self.current_money, 100)
        pygame.draw.polygon(screen,
                            [255, 160, 0],
                            Launcher._create_launch_strip_points(self, ball_radius, height_money, screen))

        height_launch_speed = min(self.launch_speed * ((-100) / max_speed), 100)
        pygame.draw.polygon(screen,
                            [5, 100, 200],
                            Launcher._create_launch_strip_points(self, ball_radius, height_launch_speed, screen))



        # Conditions
        enough_money = self.current_money >= self.launch_cost
        enough_time_has_passed = (time - self.last_launch) >= 2 * clock_tick
        blinking_condition = math.cos(0.15 * time) > 0.0

        if enough_money and enough_time_has_passed and blinking_condition:
            pygame.draw.circle(screen, (255, 160, 0), [start_pos.x, start_pos.y], ball_radius)

        key = pygame.key.get_pressed()

        if key[pygame.K_UP] is True and enough_money and enough_time_has_passed:
            self.trigger = True
            self.launch_speed += (-20) / clock_tick

        elif self.trigger:
            if self.launch_speed >= (max_speed * 1):
                self.launch_speed = (max_speed * 1)

            position: Vector = Vector(start_pos.x, start_pos.y)
            speed: Vector = Vector(0, self.launch_speed)
            mass = 170
            random_color = [200 * random.random() + 50, 200 * random.random() + 50, 200 * random.random() + 50]

            Ball(position, speed, ball_radius, mass, random_color, self.score_tracker, True)
            self.last_launch = time
            self.trigger = False

            self.current_money = 0
            self.launch_speed = 0
