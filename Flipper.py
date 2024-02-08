import math

import pygame

from Polygon import Polygon
import ScoreTracker
from Vector import Vector


class Flipper(Polygon):
    """
    Represents the flippers of the game
    """
    default_speed = Vector(0, 0)
    default_angle_speed = 0.0
    default_loss = 0
    default_movement = True
    default_score_points = 0

    def __init__(self, pos: list[Vector], pivot_point: Vector, color: list[int],
                 key, max_angle_speed, score_tracker: ScoreTracker):

        super().__init__(pos, pivot_point, Flipper.default_speed,
                         color, score_tracker, Flipper.default_score_points, Flipper.default_angle_speed,
                         Flipper.default_loss, Flipper.default_movement)
        self.angle = 0
        self.key = key
        self.max_angle_speed = max_angle_speed

    def update(self, screen, dt):
        key = pygame.key.get_pressed()
        if key[self.key]:
            self.angle_speed = self.max_angle_speed
            if abs(self.angle) > 1:
                self.angle_speed = 0.0

        elif math.isclose(abs(self.angle), 0, abs_tol=0.001):
            self.angle_speed = 0
        else:
            self.angle_speed = -self.max_angle_speed
        self.angle += self.angle_speed * dt
        super().update(screen, dt)
