import math
import pygame

from GameObject import GameObject
import ScoreTracker
from Vector import Vector, length, dot, normalize, vector_to_tupel


class Polygon(GameObject):
    """
    This class represents a polygon with n vertices. The polygons should always be drawn in an anti-clockwise direction.
    """
    Polygons = []
    big_integer = 1000000

    def __init__(self, pos: list[Vector], pivot_point: Vector, speed: Vector, color: list[int],
                 score_tracker: ScoreTracker, score_points: int = 1,
                 angle_speed=0, loss=0.1, movable=False, oscillator=None):
        """
        The initialization method
        Arguments:
            pos: A vector representing the vertices of the polygon
            pivot_point: The point at which the polygon is rotated
            speed: the speed of the polygon
            color: the color of the polygon
            score_tracker: The object used to track the score when a ball collides with a polygon
            angle_speed: the speed at which the polygon is rotated
            loss: the amount of speed the ball loses when a ball collides with a polygon
            movable: if the polygon is can be moved by collisions or not. True is movable, false not.
            oscillator: if the polygon constantly moves
        """
        super().__init__(pos, speed, movable, oscillator)
        self.size = len(pos)
        self.vertices = []
        for i in range(self.size):
            self.vertices.append(pos[i])
        self.edges = []

        self.loss = loss
        self.pivot_point = pivot_point
        self.speed = speed
        self.color = color
        self.angle_speed = angle_speed
        self.movable = movable
        self._calculate_edges()
        self.score_tracker: ScoreTracker = score_tracker
        self.score_points = score_points
        Polygon.Polygons.append(self)

    def _calculate_edges(self):
        """
        Calculates the edges of the polygon.
        """
        self.edges = []
        for vertex in range(self.size):
            if vertex == self.size - 1:
                # vector between self.size[vertex] and self.size[0]
                self.edges.append(self.vertices[0] - self.vertices[vertex])
            else:
                # vector between self.size[vertex] and self.size[vertex + 1]
                self.edges.append(self.vertices[vertex + 1] - self.vertices[vertex])

    def move(self, distance):
        """
        Move the polygon (translation) given distance.
        :param distance: the distance to move the polygon.
        """
        if self.movable:
            for i in range(len(self.vertices)):
                self.vertices[i] = self.vertices[i] + distance
            self.pivot_point += distance

    def _rotate(self, angle):
        """
        Rotates the polygon by the given angle
        :param angle: The angle to rotate the polygon
        """
        if self.movable:
            for i in range(len(self.vertices)):
                self.vertices[i] = self.vertices[i] - self.pivot_point
                self.vertices[i].rotate(angle)
                self.vertices[i] = self.vertices[i] + self.pivot_point

    def _calculate_slope(self, edge):
        """
        Calculates the slope of an edge in the polygon.
        :param edge: The edge which slope is being calculated
        """
        small_float = 1 / Polygon.big_integer
        if math.isclose(edge.x, 0):
            slope = Polygon.big_integer
        elif math.isclose(edge.y, 0):
            slope = small_float
        else:
            slope = edge.y / edge.x
        return slope

    def _collision_detection(self, dt, ball):
        """
        Collision detection from a ball with this (self) polygon.
        :param dt: The time with which the ball is going to move to collision perimeter
        :param ball: The ball which is going to move to collision perimeter
        """
        new_ball_position: Vector = ball.pos + ball.speed * dt
        collision_with_smallest_distance = None
        best_collision_edge = None
        best_collision_vector = None

        for i in range(self.size):
            edge = self.edges[i]
            edge_source_vertex = self.vertices[i]
            edge_target_vertex = edge_source_vertex + edge
            slope = self._calculate_slope(edge)

            # values needed for collision detection
            edge_line_y_axis_intersection = edge_source_vertex.y - slope * edge_source_vertex.x
            ball_line_y_axis_intersection = new_ball_position.y + 1 / slope * new_ball_position.x

            collision_point_x = (-edge_line_y_axis_intersection + ball_line_y_axis_intersection) / (slope + 1 / slope)
            collision_point_y = slope * collision_point_x + edge_source_vertex.y - slope * edge_source_vertex.x
            collision_vector = Vector(collision_point_x, collision_point_y)

            distance = length(new_ball_position - collision_vector)
            distance_source_vertex_to_collision_vector = length(collision_vector - edge_source_vertex)
            distance_target_vertex_to_collision_vector = length(collision_vector - edge_target_vertex)
            edge_length = length(edge)
            ball_radius_corner_approximation = ball.radius * (1 / math.sqrt(2))
            # collision conditions
            ball_radius_close_to_edge = distance <= ball.radius
            ball_near_enough_to_polygon = ((distance_source_vertex_to_collision_vector
                                            + distance_target_vertex_to_collision_vector - edge_length)
                                           <= ball_radius_corner_approximation)

            if ball_radius_close_to_edge and ball_near_enough_to_polygon:
                if (collision_with_smallest_distance is None) or (distance <= collision_with_smallest_distance):
                    collision_with_smallest_distance = distance
                    best_collision_edge = edge
                    best_collision_vector = collision_vector
        return best_collision_edge, best_collision_vector

    def _collide(self, dt, ball, collision_edge: Vector, collision_vector: Vector, launcher):
        if collision_edge is not None:
            new_ball_position: Vector = ball.pos + ball.speed * dt
            collision_point = Vector(collision_vector.x, collision_vector.y)

            turning_radius = collision_point - self.pivot_point
            speed_polygon = turning_radius * self.angle_speed
            speed_polygon = self.speed + (Vector.rotate(speed_polygon, (math.pi / 2)))
            normale = normalize(new_ball_position - collision_point)
            speed_normal = dot(speed_polygon, normale)
            if speed_normal <= 0:
                speed_normal = 0
            if ball.movable:
                ball.speed = ball.speed + normale * (2 * abs(dot(ball.speed, normale)) *(1-self.loss) + speed_normal)
                ball.pos = ball.pos + normalize(new_ball_position - collision_point) * 1
            self.score_tracker.update(self.score_points)
            launcher.current_money += 2

    def validate_collision(self, dt, ball, launcher):
        collision_edge, collision_vector = self._collision_detection(dt, ball)
        self._collide(dt, ball, collision_edge, collision_vector, launcher)


    def update(self, screen, dt):
        if self.movable:
            self._rotate(self.angle_speed * dt)
            self.move(self.speed * dt)
            self._calculate_edges()
        vertices_points = []
        self.oscillate()
        for i in range(self.size):
            vertices_points.append(vector_to_tupel(self.vertices[i]))
        pygame.draw.polygon(screen, (self.color[0], self.color[1], self.color[2]), vertices_points)
