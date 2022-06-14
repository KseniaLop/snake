import pygame
import time
import random

import game_data as gd
import domain

pygame.init()
pygame.mixer.music.load('audio/background-music.ogg')
pygame.mixer.music.play(-1)

pygame.display.set_caption(gd.GAME_DATA.get_window_title())
GAME_WINDOW = pygame.display.set_mode((gd.GAME_DATA.get_window_width(),
                                       gd.GAME_DATA.get_window_height()))


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
    pygame.mixer.music.pause()

    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    paused = False
                    pygame.mixer.music.unpause()
                elif e.key == pygame.K_q:
                    quit()

        GAME_WINDOW.fill(gd.GameColor.WHITE.value)
        message_to_screen("Paused",
                          gd.GameColor.SKY.value,
                          -100,
                          'large',
                          gd.GAME_DATA.get_window_width(),
                          gd.GAME_DATA.get_window_height())
        message_to_screen("Нажми C, чтобы продолжить, или Q, чтобы выйти",
                          gd.GameColor.SKY.value,
                          25,
                          'small',
                          gd.GAME_DATA.get_window_width(),
                          gd.GAME_DATA.get_window_height())
        pygame.display.update()
        pygame.time.Clock().tick(5)


def generate_food():
    x = random.randrange(1, (gd.GAME_DATA.get_window_width() // 10)) * 10
    y = random.randrange(1, (gd.GAME_DATA.get_window_height() // 10)) * 10

    gd.FRUIT_POSITION = (x, y)
    gd.FRUIT_BUFF_FUNC = domain.get_random_fruit_buff()


def respawn():
    time.sleep(0.5)

    gd.SNAKE_POSITION = gd.GAME_DATA.get_default_snake_position()
    gd.SNAKE_BODY = gd.GAME_DATA.get_default_snake_body()
    gd.DIRECTION = gd.GAME_DATA.get_default_direction()
    gd.CHANGE_TO = gd.DIRECTION

    generate_food()


def game_over():
    message_to_screen("Your score is: " + str(gd.SCORE),
                      gd.GameColor.WHITE.value,
                      0,
                      'small',
                      gd.GAME_DATA.get_window_width(),
                      gd.GAME_DATA.get_window_height())
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()


while not gd.GAME_EXIT:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gd.CHANGE_TO = gd.Direction.UP.value
            if event.key == pygame.K_DOWN:
                gd.CHANGE_TO = gd.Direction.DOWN.value
            if event.key == pygame.K_LEFT:
                gd.CHANGE_TO = gd.Direction.LEFT.value
            if event.key == pygame.K_RIGHT:
                gd.CHANGE_TO = gd.Direction.RIGHT.value
            if event.key == pygame.K_p:
                pause()
        if event.type == pygame.QUIT:
            gd.GAME_EXIT = True

    if gd.CHANGE_TO == gd.Direction.UP.value and gd.DIRECTION != gd.Direction.DOWN.value:
        gd.DIRECTION = gd.Direction.UP.value
    if gd.CHANGE_TO == gd.Direction.DOWN.value and gd.DIRECTION != gd.Direction.UP.value:
        gd.DIRECTION = gd.Direction.DOWN.value
    if gd.CHANGE_TO == gd.Direction.LEFT.value and gd.DIRECTION != gd.Direction.RIGHT.value:
        gd.DIRECTION = gd.Direction.LEFT.value
    if gd.CHANGE_TO == gd.Direction.RIGHT.value and gd.DIRECTION != gd.Direction.LEFT.value:
        gd.DIRECTION = gd.Direction.RIGHT.value

    if gd.DIRECTION == gd.Direction.UP.value:
        gd.SNAKE_POSITION[1] -= 10
    if gd.DIRECTION == gd.Direction.DOWN.value:
        gd.SNAKE_POSITION[1] += 10
    if gd.DIRECTION == gd.Direction.LEFT.value:
        gd.SNAKE_POSITION[0] -= 10
    if gd.DIRECTION == gd.Direction.RIGHT.value:
        gd.SNAKE_POSITION[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    gd.SNAKE_BODY.insert(0, tuple(gd.SNAKE_POSITION))
    if gd.SNAKE_POSITION[0] == gd.FRUIT_POSITION[0] and gd.SNAKE_POSITION[1] == gd.FRUIT_POSITION[1]:
        gd.SCORE += 10
        gd.GAME_SPEED = gd.GAME_DATA.get_default_game_speed()
        gd.FRUIT_BUFF_FUNC()
        gd.FRUIT_SPAWN = False
    else:
        gd.SNAKE_BODY.pop()

    if not gd.FRUIT_SPAWN:
        generate_food()
        gd.FRUIT_SPAWN = True

    GAME_WINDOW.fill(gd.GameColor.SKY.value)

    for cell in gd.SNAKE_BODY:
        pygame.draw.rect(GAME_WINDOW, gd.GameColor.ORANGE.value,
                         pygame.Rect(cell[0], cell[1], 10, 10))
    pygame.draw.rect(GAME_WINDOW, gd.FRUIT_COLOR, pygame.Rect(
        gd.FRUIT_POSITION[0], gd.FRUIT_POSITION[1], 10, 10))

    if gd.SNAKE_POSITION[0] < 0 or gd.SNAKE_POSITION[0] > gd.GAME_DATA.get_window_width() - 10 or \
            gd.SNAKE_POSITION[1] < 0 or gd.SNAKE_POSITION[1] > gd.GAME_DATA.get_window_height() - 10:
        if gd.LIVES == 1:
            game_over()
        else:
            gd.LIVES -= 1
            respawn()

    # Touching the snake body
    for cell in gd.SNAKE_BODY[1:]:
        if gd.SNAKE_POSITION[0] == cell[0] and gd.SNAKE_POSITION[1] == cell[1]:
            if gd.LIVES == 1:
                game_over()
            else:
                gd.LIVES -= 1
                respawn()

    message_to_screen("Score: " + str(gd.SCORE),
                      gd.GameColor.WHITE.value, 10, 'small',
                      gd.SCORE_TEXT_POSITION[0], gd.SCORE_TEXT_POSITION[1])
    message_to_screen("Lives: " + str(gd.LIVES),
                      gd.GameColor.WHITE.value, 10, 'small',
                      gd.LIVES_TEXT_POSITION[0], gd.LIVES_TEXT_POSITION[1])
    pygame.display.update()
    pygame.time.Clock().tick(gd.GAME_SPEED)


pygame.quit()
quit()
