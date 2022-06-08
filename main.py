import pygame
import time
import random

from domain import *


GAME_DATA = DefaultGameData()

GAME_SPEED = GAME_DATA.get_default_game_speed()

pygame.init()

pygame.display.set_caption(GAME_DATA.get_window_title())
GAME_WINDOW = pygame.display.set_mode((GAME_DATA.get_window_width(), GAME_DATA.get_window_height()))

SCORE_TEXT_POSITION = GAME_DATA.get_score_text_position()
LIVES_TEXT_POSITION = GAME_DATA.get_lives_text_position()

SNAKE_POSITION = [100, 50]

SNAKE_BODY = [(100, 50),
              (90, 50),
              (80, 50),
              (70, 50)]

FRUIT_POSITION = (random.randrange(1, (GAME_DATA.get_window_width() // 10)) * 10,
                  random.randrange(1, (GAME_DATA.get_window_height() // 10)) * 10)
FRUIT_SPAWN = True

DIRECTION = GAME_DATA.get_default_direction()
CHANGE_TO = DIRECTION

SCORE = GAME_DATA.get_default_score()
LIVES = GAME_DATA.get_default_lives()

GAME_EXIT = False


def text_objects(text, color, size):
    value_size = {'small': 25, 'medium': 50, 'large': 75}.get(size)
    font = pygame.font.SysFont('comicsansms', value_size)
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace, size, win_x, win_y):
    text_surface, text_rect = text_objects(msg, color, size)
    x = win_x
    y = win_y
    text_rect.center = (x / 2), (y / 2) + y_displace
    GAME_WINDOW.blit(text_surface, text_rect)


def pause():
    paused = True
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    paused = False
                elif e.key == pygame.K_q:
                    quit()

        GAME_WINDOW.fill(GameColor.WHITE.value)
        message_to_screen("Paused",
                          GameColor.BLACK.value,
                          -100,
                          'large',
                          GAME_DATA.get_window_width(),
                          GAME_DATA.get_window_height())
        message_to_screen("Нажми C, чтобы продолжить, или Q, чтобы выйти",
                          GameColor.BLACK.value,
                          25,
                          'small',
                          GAME_DATA.get_window_width(),
                          GAME_DATA.get_window_height())
        pygame.display.update()
        pygame.time.Clock().tick(5)


def generate_food():
    global FRUIT_POSITION

    x = random.randrange(1, (GAME_DATA.get_window_width() // 10)) * 10
    y = random.randrange(1, (GAME_DATA.get_window_height() // 10)) * 10

    FRUIT_POSITION = (x, y)


def respawn():
    global SNAKE_POSITION
    global SNAKE_BODY
    global DIRECTION
    global CHANGE_TO

    time.sleep(0.5)

    SNAKE_POSITION = GAME_DATA.get_default_snake_position()
    SNAKE_BODY = GAME_DATA.get_default_snake_body()
    DIRECTION = GAME_DATA.get_default_direction()
    CHANGE_TO = DIRECTION

    generate_food()


def game_over():
    message_to_screen("Your score is: " + str(SCORE),
                      GameColor.WHITE.value,
                      0,
                      'small',
                      GAME_DATA.get_window_width(),
                      GAME_DATA.get_window_height())
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()


while not GAME_EXIT:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                CHANGE_TO = Direction.UP.value
            if event.key == pygame.K_DOWN:
                CHANGE_TO = Direction.DOWN.value
            if event.key == pygame.K_LEFT:
                CHANGE_TO = Direction.LEFT.value
            if event.key == pygame.K_RIGHT:
                CHANGE_TO = Direction.RIGHT.value
            if event.key == pygame.K_p:
                pause()
        if event.type == pygame.QUIT:
            GAME_EXIT = True

    if CHANGE_TO == 'UP' and DIRECTION != 'DOWN':
        DIRECTION = 'UP'
    if CHANGE_TO == 'DOWN' and DIRECTION != 'UP':
        DIRECTION = 'DOWN'
    if CHANGE_TO == 'LEFT' and DIRECTION != 'RIGHT':
        DIRECTION = 'LEFT'
    if CHANGE_TO == 'RIGHT' and DIRECTION != 'LEFT':
        DIRECTION = 'RIGHT'

    if DIRECTION == 'UP':
        SNAKE_POSITION[1] -= 10
    if DIRECTION == 'DOWN':
        SNAKE_POSITION[1] += 10
    if DIRECTION == 'LEFT':
        SNAKE_POSITION[0] -= 10
    if DIRECTION == 'RIGHT':
        SNAKE_POSITION[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    SNAKE_BODY.insert(0, tuple(SNAKE_POSITION))
    if SNAKE_POSITION[0] == FRUIT_POSITION[0] and SNAKE_POSITION[1] == FRUIT_POSITION[1]:
        SCORE += 10
        FRUIT_SPAWN = False
    else:
        SNAKE_BODY.pop()

    if not FRUIT_SPAWN:
        generate_food()
        FRUIT_SPAWN = True

    GAME_WINDOW.fill(GameColor.BLACK.value)

    for cell in SNAKE_BODY:
        pygame.draw.rect(GAME_WINDOW, GameColor.GREEN.value,
                         pygame.Rect(cell[0], cell[1], 10, 10))
    pygame.draw.rect(GAME_WINDOW, GameColor.WHITE.value, pygame.Rect(
        FRUIT_POSITION[0], FRUIT_POSITION[1], 10, 10))

    if SNAKE_POSITION[0] < 0 or SNAKE_POSITION[0] > GAME_DATA.get_window_width() - 10 or \
            SNAKE_POSITION[1] < 0 or SNAKE_POSITION[1] > GAME_DATA.get_window_height() - 10:
        if LIVES == 1:
            game_over()
        else:
            LIVES -= 1
            respawn()

    # Touching the snake body
    for cell in SNAKE_BODY[1:]:
        if SNAKE_POSITION[0] == cell[0] and SNAKE_POSITION[1] == cell[1]:
            if LIVES == 1:
                game_over()
            else:
                LIVES -= 1
                respawn()

    message_to_screen("Score: " + str(SCORE),
                      GameColor.WHITE.value, 10, 'small',
                      SCORE_TEXT_POSITION[0], SCORE_TEXT_POSITION[1])
    message_to_screen("Lives: " + str(LIVES),
                      GameColor.WHITE.value, 10, 'small',
                      LIVES_TEXT_POSITION[0], LIVES_TEXT_POSITION[1])
    pygame.display.update()
    pygame.time.Clock().tick(GAME_SPEED)


pygame.quit()
quit()
