import pygame

from Polygon import Polygon
import ScoreTracker
from Vector import Vector


class Flipper(Polygon):
    default_speed = Vector(0, 0)
    default_angle_speed = 0.0
    default_loss = 0
    default_movement = True

    def __init__(self, pos: list[Vector], pivot_point: Vector, color: list[int],
                 key, max_angle_speed, score_tracker: ScoreTracker):

        super().__init__(pos, pivot_point, Flipper.default_speed,
                         color, score_tracker, Flipper.default_angle_speed,
                         Flipper.default_loss, Flipper.default_movement)
        self.angle = 0
        self.key = key
        self.max_angle_speed = max_angle_speed

    def update(self, screen, dt):  # todo:V(F)
        key = pygame.key.get_pressed()
        if key[self.key]:
            self.angle_speed = self.max_angle_speed
            # brake by 90 degrees
            if self.angle > 1:
                self.angle_speed = 0.0
            # brake by -90 degrees
            elif self.angle < -1:
                self.angle_speed = 0.0

        elif (self.angle ** 2) - 0.001 <= 0.001:
            self.angle_speed = 0
        else:
            self.angle_speed = -self.max_angle_speed
        self.angle += self.angle_speed * dt
        super().update(screen, dt)
