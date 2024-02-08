import pygame


class ScoreTracker:
    """ This class represents a score tracker. It keeps track of the score in a game of pinball."""
    initial_score = 0
    default_font = 'freesansbold.ttf'
    default_font_size = 32
    score_display_text_prefix = "Score: "
    color = (255, 255, 255)
    postion_x = 35
    postion_y = 15

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.score = ScoreTracker.initial_score
        self.font = pygame.font.Font(ScoreTracker.default_font, ScoreTracker.default_font_size)

    def get_score(self):
        return self.score

    def update(self, score_points: int):
        self.score += score_points

    def show(self):
        score_display_text = ScoreTracker.score_display_text_prefix + str(self.score)
        current_score = self.font.render(score_display_text, True, ScoreTracker.color)
        self.screen.blit(current_score, (self.postion_x, self.postion_y))
