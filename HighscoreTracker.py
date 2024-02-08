import os
from pathlib import Path
import pickle
import pygame

from ScoreTracker import ScoreTracker


class HighscoreTracker:
    """
    Represents an object that tracks the highscores of the games that have been played. It keeps the ten highest scores.
    """
    highscore_save_file_path = Path(__file__).parents[0] / Path("highscores.pickle")
    amount_of_highscores_saved = 10
    new_line = "\n"
    print_format_prefix = "-----Highscores-----" + new_line
    order_punctuation = ")"
    highscore_score_display_length = 30

    default_font = 'freesansbold.ttf'
    default_font_size = 32
    color = (255, 255, 255)
    postion_x = 130
    postion_y = 200

    def __init__(self, screen: pygame.surface, score_tracker: ScoreTracker):
        self.font = pygame.font.Font(ScoreTracker.default_font, ScoreTracker.default_font_size)
        self.screen = screen
        self.score_tracker = score_tracker
        self.current_highscore_list = self._read_highscore_save_file()

    def __str__(self):
        highscores = self.current_highscore_list
        print_format = HighscoreTracker.print_format_prefix
        index = 1
        for score in highscores:
            size_of_punctuation = (HighscoreTracker.highscore_score_display_length
                                   - (len(str(index)) * 2 + len(str(score))))
            punctuation = ""
            for _ in range(size_of_punctuation):
                punctuation += "."

            print_format += (str(index) + HighscoreTracker.order_punctuation + punctuation +
                             str(score) + HighscoreTracker.new_line)
            index += 1
        return print_format.strip()

    def _write_highscore_save_file(self):
        with open(HighscoreTracker.highscore_save_file_path, 'wb') as fp:
            pickle.dump(self.current_highscore_list, fp)
            print('Done writing list into a binary file')

    def _read_highscore_save_file(self):
        current_highscore_list = []
        if os.path.isfile(HighscoreTracker.highscore_save_file_path):
            with open(HighscoreTracker.highscore_save_file_path, 'rb') as fp:
                current_highscore_list = pickle.load(fp)
        return current_highscore_list

    def render_multi_line(self):
        lines = str(self).splitlines()
        for i, l in enumerate(lines):
            self.screen.blit(self.font.render(l, 0, HighscoreTracker.color),
                             (HighscoreTracker.postion_x, HighscoreTracker.postion_y + self.font.get_linesize() * i))

    def update(self):
        this_game_score = self.score_tracker.get_score()
        self.current_highscore_list.append(this_game_score)
        self.current_highscore_list.sort(reverse=True)
        self.current_highscore_list = self.current_highscore_list[:HighscoreTracker.amount_of_highscores_saved]
        self._write_highscore_save_file()
