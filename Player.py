import pygame


class Player:
    """
    Represents a player. Keeps track of the amount of life a player has.
    """
    default_font = 'freesansbold.ttf'
    default_font_size = 32
    life_display_text_prefix = "Lives: "
    color = (255, 255, 255)
    position_x = 35
    position_y = 50

    def __init__(self, life, screen: pygame.Surface):

        self.life = life
        self.screen = screen
        self.font = pygame.font.Font(Player.default_font, Player.default_font_size)

    def loose_life(self, ball_pos, s_height):
        if ball_pos >= s_height:
            self.life -= 1
            return True
        return False

    def is_not_alive(self):
        if self.life >= 1:
            return False
        return True

    def show(self):
        life_display_text = Player.life_display_text_prefix + str(self.life)
        current_lives = self.font.render(life_display_text, True, Player.color)
        self.screen.blit(current_lives, (Player.position_x, Player.position_y))
