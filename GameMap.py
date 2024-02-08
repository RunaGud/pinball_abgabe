import math
import pygame

from Ball import Ball
from Flipper import Flipper
from Polygon import Polygon
import ScoreTracker
from Vector import Vector


class GameMap:
    """
    This class represents a set of objects on a game instance.
    """

    def __init__(self, ball_radius, screen: pygame.Surface, score_tracker: ScoreTracker):
        self.ball_radius = ball_radius
        self.screen = screen
        self.score_tracker = score_tracker

    def initialize_map(self):
        # Essential Points:
        s_width, s_height = self.screen.get_width(), self.screen.get_height()
        ball_radius = self.ball_radius
        score_tracker = self.score_tracker
        pivot_point_flipper_height = s_height * 0.9
        pivot_point_flipper_with_part = 0.3
        pivot_point_right = Vector(s_width * (1 - pivot_point_flipper_with_part), pivot_point_flipper_height)
        pivot_point_left = Vector(pivot_point_flipper_with_part * s_width, pivot_point_flipper_height)
        flipper_thickness = 14

        # fall_probability
        # is the number of balls_radius fit between the flipper Vector(s_width/2-fall_probability,flipper_downed -2*dt)
        fall_probability = ball_radius * 1.4
        flipper_downed = s_height * 0.96

        left_flipper = Flipper(
            [Vector(pivot_point_left.x - 2 * flipper_thickness, pivot_point_left.y),
             Vector(pivot_point_left.x - flipper_thickness * 1, pivot_point_left.y + flipper_thickness * 2),
             Vector(s_width / 2 - fall_probability, flipper_downed),
             Vector(s_width / 2 - fall_probability, flipper_downed - 1 * flipper_thickness)],
            Vector(pivot_point_left.x, pivot_point_left.y),
            [250, 250, 0],
            pygame.K_LEFT,
            0.15,
            score_tracker)

        right_flipper = Flipper(
            [Vector(s_width / 2 + fall_probability, flipper_downed - flipper_thickness),
             Vector(s_width / 2 + fall_probability, flipper_downed),
             Vector(pivot_point_right.x + flipper_thickness * 1, pivot_point_right.y + 2 * flipper_thickness),
             Vector(pivot_point_right.x + 2 * flipper_thickness, pivot_point_right.y)],
            Vector(pivot_point_right.x, pivot_point_right.y),
            [250, 250, 0],
            pygame.K_RIGHT,
            -0.15,
            score_tracker)

        lower_left_corner = Polygon([Vector(0, s_height), Vector(s_width * 0.3, s_height), pivot_point_left,
                                     Vector(s_width * 0.16, s_height * 0.85), Vector(0, s_height * 0.82)],
                                    Vector(121, 200),
                                    Vector(0, 0),
                                    [250, 50, 50],
                                    score_tracker,
                                    0,
                                    0,
                                    0.25,
                                    False)

        lower_right_corner = Polygon([Vector(s_width, s_height * 0.82), Vector(s_width * 0.84, s_height * 0.85),
                                      pivot_point_right, Vector(s_width * 0.7, s_height), Vector(s_width, s_height)],
                                     Vector(121, 200),
                                     Vector(0, 0),
                                     [250, 50, 50],
                                     score_tracker,
                                     0,
                                     0,
                                     0.25,
                                     False)

        rotating_triangle = Polygon([Vector(200, 500), Vector(400, 500), Vector(300, 400)],
                                    Vector(300, 450),
                                    Vector(0, 0),
                                    [200, 200, 250],
                                    score_tracker,
                                    1,
                                    0.1,
                                    0.0,
                                    True)

        launcher_line = Polygon([Vector(s_width - ball_radius * 2.5, s_height * 0.76),
                                 Vector(s_width - ball_radius * 2.5, s_height * 0.2),
                                 Vector(s_width * 1 - ball_radius * 4, s_height * 0.2),
                                 Vector(s_width * 1 - ball_radius * 4, s_height * 0.76)],
                                Vector(121, 200),
                                Vector(0, 0),
                                [250, 250, 50],
                                score_tracker,
                                0,
                                0,
                                0.3,
                                False)

        upper_right_corner = Polygon([Vector(s_width - 3 * ball_radius, 0),
                                      Vector(s_width, 3 * ball_radius), Vector(s_width, 0)],
                                     Vector(121, 200),
                                     Vector(0, 0),
                                     [50, 250, 50],
                                     score_tracker,
                                     5,
                                     0,
                                     0.3,
                                     False)

        upper_left_corner = Polygon([Vector(0, 0), Vector(0, 3 * ball_radius), Vector(3 * ball_radius, 0)],
                                    Vector(121, 200),
                                    Vector(0, 0),
                                    [50, 250, 50],
                                    score_tracker,
                                    5,
                                    0,
                                    0.3,
                                    False)
        in_length = 3 * ball_radius
        out_length = in_length + 1.1 * ball_radius
        between = 1 / math.sqrt(2)
        moon_oscillator = [lambda t: 2 * (math.cos(t * 0.01) * (math.cos(0.005 * t) + 2)), None]
        moon = Polygon([Vector(s_width * 0.3 - in_length, s_height * 0.3 - 1.3 * ball_radius),
                        Vector(s_width * 0.3 - in_length * between, s_height * 0.3 - in_length * between),
                        Vector(s_width * 0.3, s_height * 0.3 - in_length),
                        Vector(s_width * 0.3 + between * in_length, s_height * 0.3 - in_length * between),
                        Vector(s_width * 0.3 + in_length, s_height * 0.3),
                        Vector(s_width * 0.3 + between * in_length, s_height * 0.3 + in_length * between),
                        Vector(s_width * 0.3, s_height * 0.3 + in_length),
                        Vector(s_width * 0.3 - between * in_length, s_height * 0.3 + in_length * between),
                        Vector(s_width * 0.3 - in_length, s_height * 0.3 + 1.3 * ball_radius),
                        Vector(s_width * 0.3 - out_length, s_height * 0.3 + 1.3 * ball_radius),
                        Vector(s_width * 0.3 - between * out_length, s_height * 0.3 + out_length * between),
                        Vector(s_width * 0.3, s_height * 0.3 + out_length),
                        Vector(s_width * 0.3 + between * out_length, s_height * 0.3 + out_length * between),
                        Vector(s_width * 0.3 + out_length, s_height * 0.3),
                        Vector(s_width * 0.3 + between * out_length, s_height * 0.3 - out_length * between),
                        Vector(s_width * 0.3, s_height * 0.3 - out_length),
                        Vector(s_width * 0.3 - between * out_length, s_height * 0.3 - out_length * between),
                        Vector(s_width * 0.3 - out_length, s_height * 0.3 - 1.3 * ball_radius)],
                       Vector(s_width * 0.3, s_height * 0.3),
                       Vector(0, 0),
                       [0, 250, 250],
                       score_tracker,
                       1,
                       0.03,
                       0.5,
                       True,
                       moon_oscillator)
        moon.move(Vector(s_width * 0.1, 0))

        floating_square_oscillator = [None, lambda t: 4 * math.sin(0.01 * t)]
        floating_square = Polygon([Vector(30 + ball_radius * 0.1, 300), Vector(80 + ball_radius * 0.1, 300),
                                   Vector(80 + ball_radius * 0.1, 200), Vector(30 + ball_radius * 0.1, 200)],
                                  Vector(55, 250),
                                  Vector(0, 0),
                                  [200, 200, 250],
                                  score_tracker,
                                  3,
                                  0.0,
                                  0.05,
                                  True,
                                  floating_square_oscillator)
        floating_square.move(Vector(0, 80))

        blue_ball_oscillator = [lambda t: 50 * 0.06 * math.cos(0.03 * t), None]
        oscillating_blue_ball = Ball(Vector(300, 100),
                                     Vector(0, 0),
                                     ball_radius * 2,
                                     20,
                                     [0, 255, 255],
                                     score_tracker,
                                     False,
                                     blue_ball_oscillator)
