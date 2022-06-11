from domain import *


GAME_DATA = DefaultGameData()

GAME_SPEED = GAME_DATA.get_default_game_speed()

SCORE_TEXT_POSITION = GAME_DATA.get_score_text_position()
LIVES_TEXT_POSITION = GAME_DATA.get_lives_text_position()

SNAKE_POSITION = [100, 50]

SNAKE_BODY = [(100, 50),
              (90, 50),
              (80, 50),
              (70, 50)]

FRUIT_COLOR = GameColor.WHITE.value
FRUIT_BUFF_FUNC = get_random_fruit_buff()
FRUIT_POSITION = (random.randrange(1, (GAME_DATA.get_window_width() // 10)) * 10,
                  random.randrange(1, (GAME_DATA.get_window_height() // 10)) * 10)
FRUIT_SPAWN = True

DIRECTION = GAME_DATA.get_default_direction()
CHANGE_TO = DIRECTION

SCORE = GAME_DATA.get_default_score()
LIVES = GAME_DATA.get_default_lives()

GAME_EXIT = False
