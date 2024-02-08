import math
import pygame

from GameObject import GameObject
import Player
from Polygon import Polygon
import ScoreTracker
from Vector import Vector, length, smallest_angle, dot, normalize


class Ball(GameObject):
    """
    This class represents a ball.
    """
    Balls = []

    def __init__(self, pos, speed, radius, mass, color, score_tracker: ScoreTracker, movable=True):
        super().__init__(pos, speed, movable)
        self.radius = radius
        self.mass = mass
        self.color = color
        Ball.Balls.append(self)
        self.score_tracker: ScoreTracker = score_tracker

    def update(self, screen: pygame.Surface, dt, gravity, loss, max_speed, launcher,
               player: Player):  # todo :to much ifs
        """
        Updates a Ball. Performs collisions with other Balls and with the walls.
        Arguments:
            self(Ball): The ball object to be updated
            screen(Surface): The screen
            dt(float): The time
            gravity(Vector): Vector that represents gravity on the game
            loss(float): The amount of speed lost after collision
            max_speed(float): Maximum speed
            launcher(Launcher): The launcher of the game
            player(Player): The player who is playing
        """

        tolerance = 2
        prev_collide = False
        if player.loose_life(self.pos.y, screen.get_height()):
            Ball.Balls.remove(self)

        elif self.pos.y - self.radius <= tolerance:
            self.speed.y = abs(self.speed.y) * (1 - loss)

        if self.pos.x + self.radius >= screen.get_width() - tolerance:
            self.speed.x = -abs(self.speed.x) * (1 - loss)
        elif self.pos.x - self.radius <= tolerance:
            self.speed.x = abs(self.speed.x) * (1 - loss)

        # Set Speed of immovable Objects to 0
        if self.movable:
            self.speed += gravity * dt
            self.pos += self.speed * dt + gravity * 0.5 * dt ** 2
            if length(self.speed) >= max_speed:
                self.speed = normalize(self.speed) * max_speed
        else:
            self.mass = 10000
            self.pos += self.speed

        # Draw Balls
        pygame.draw.circle(screen,
                           (self.color[0], self.color[1], self.color[2]),
                           [self.pos.x, self.pos.y],
                           self.radius)

        # Detect Collisions between two balls

        for j in Ball.Balls:
            if self == j:
                continue
            ipos1 = self.pos + self.speed * dt
            jpos1 = j.pos + j.speed * dt
            if length(ipos1 - jpos1) <= (self.radius + j.radius) and not prev_collide:
                prev_collide = True
                self.score_tracker.update()
                collide(self, j, loss, dt)

            else:
                prev_collide = False

        # collision between ball and polygon

        for p in Polygon.Polygons:
            p.validate_collision(dt, self, launcher)


def collide(b1, b2, loss, dt):
    """
    Performs a collision between two balls
    Arguments:
            b1 (Ball): first Ball to perform collision
            b2 (Ball): second Ball to perform collision
            loss (float) : Loss between 0 or 1
            dt (float) : Time change
    Returns:
        None    
    """
    # Galileo-Transformation in the frame of reference, at which the ball b2 is.
    b1.speed = b1.speed - b2.speed
    # b1_pos is the position from b1 in the next time step
    b1_pos = b1.pos + b1.speed * dt
    # b2_pos is the position from b2 in the next time step
    b2_pos = b2.pos + b2.speed * dt
    # n is a normalized vector from the center of b1 to the center of b2
    n = normalize(b2_pos - b1_pos)
    # vt is the speed component from b1 in the direction of b2 (radial speed, projection)
    vt = abs(dot(b1.speed, n))
    # Mit dem Skalarprodukt wird die Tangentialkomponente der Geschwindigkeit von b1 ausgerechnet
    vp = abs(length(b1.speed) * math.sin(smallest_angle(b1.speed, n)))
    # vt1 after the elastic collision (Formula for elastic collision but one of the speeds is zero)
    vt1 = abs((b1.mass * vt - b2.mass * vt) / (b1.mass + b2.mass))
    # norm is n rotated in 90 degrees, for it to show on the tangential direction.
    norm = Vector(n.x, -n.y)
    if b1.movable:
        # Speed for b1 is calculated from the radial and tangential components  put together with help of n and norm.
        b1.speed = norm * vp - n * vt1
        b1.speed = b1.speed * (1 - loss)
    b1.speed = b1.speed + b2.speed
    # Radial speed for b2 (Formula for elastic collision, again with b2.speed = 0)
    vt2 = b1.mass * 2 * vt / (b1.mass + b2.mass)

    if b2.movable:
        b2.speed = n * vt2 + b2.speed
        b2.speed = b2.speed * (1 - loss)

    if b1.movable:
        b1.pos = b1.pos - n * 0.1
    if b2.movable:
        b2.pos = b2.pos + n * 0.1
