from dataclasses import dataclass
from enum import Enum
import random

from pygame import Color
import game_data as gd


def _decrease_speed():
    gd.GAME_SPEED -= 5


def _add_score():
    gd.SCORE += 10


def _add_tail():
    gd.SNAKE_BODY.append(gd.SNAKE_BODY[-1])


def get_random_fruit_buff():
    func = random.choice([_decrease_speed, _add_score, _add_tail])

    if func == _decrease_speed:
        gd.FRUIT_COLOR = GameColor.RED.value
    elif func == _add_score:
        gd.FRUIT_COLOR = GameColor.BLUE.value
    elif func == _add_tail:
        gd.FRUIT_COLOR = GameColor.PURPLE.value

    return func


class GameColor(Enum):
    WHITE = Color(255, 255, 255)
    SKY = Color(180, 207, 236)
    RED = Color(254, 77, 77)
    ORANGE = Color(255, 132, 0)
    BLUE = Color(0, 0, 255)
    PURPLE = Color(226, 56, 236)


class Direction(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'


@dataclass(frozen=True)
class DefaultGameData:
    _window_width = 720
    _window_height = 480
    _cell_size = 10
    _title = 'Snake'

    _score_text_position = (120, 20)
    _lives_text_position = (500, 20)

    _default_score = 0
    _default_lives = 3
    _default_game_speed = 15
    _default_direction = Direction.RIGHT.value

    _default_snake_position = [100, 50]
    _default_snake_body = [
        (100, 50),
        (90, 50),
        (80, 50),
        (70, 50)
    ]

    def get_window_width(self):
        return int(self._window_width)

    def get_window_height(self):
        return int(self._window_height)

    def get_cell_size(self):
        return int(self._cell_size)

    def get_window_title(self):
        return str(self._title)

    def get_score_text_position(self):
        return tuple(self._score_text_position)

    def get_lives_text_position(self):
        return tuple(self._lives_text_position)

    def get_default_score(self):
        return int(self._default_score)

    def get_default_lives(self):
        return int(self._default_lives)

    def get_default_game_speed(self):
        return int(self._default_game_speed)

    def get_default_direction(self):
        return str(self._default_direction)

    def get_default_snake_position(self):
        return list(self._default_snake_position)

    def get_default_snake_body(self):
        return list(self._default_snake_body)
