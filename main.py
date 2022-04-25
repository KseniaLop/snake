import pygame
import time
import random


snake_speed = 15

window_x = 720
window_y = 480

pygame.init()

pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


snake_position = [100, 50]

snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

fruit_position = [random.randrange(1, (window_x//10)) * 10,
                  random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

lives = 3

game_exit = False


# не используется
def show_score():
    score_surface, score_rect = text_objects("Score: " + str(score), white, 'small')
    game_window.blit(score_surface, score_rect)


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
    game_window.blit(text_surface, text_rect)


def pause():
    paused = True
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.QUIT
                quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    paused = False
                elif e.key == pygame.K_q:
                    pygame.QUIT
                    quit()

        game_window.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          'large',
                          window_x,
                          window_y)
        message_to_screen("Нажми C, чтобы продолжить, или Q, чтобы выйти",
                          black,
                          25,
                          'small',
                          window_x,
                          window_y)
        pygame.display.update()
        pygame.time.Clock().tick(5)


def game_over():
    message_to_screen("Your score is: " + str(score),
                      white,
                      0,
                      'small',
                      window_x,
                      window_y)
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()


while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_p:
                pause()
        if event.type == pygame.QUIT:
            game_exit = True

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if fruits and snakes collide then scores
    # will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # game over and lives
    if (snake_position[0] < 0 or snake_position[0] > window_x - 10) and lives == 0:
        game_over()
    #if (snake_position[0] < 0 or snake_position[0] > window_x - 10) and lives > 0:
        #lives -= 1
    if (snake_position[1] < 0 or snake_position[1] > window_y - 10) and lives == 0:
        game_over()
    #if (snake_position[1] < 0 or snake_position[1] > window_y - 10) and lives > 0:
        #lives -= 1

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1] and lives == 0:
            game_over()

    message_to_screen("Score: " + str(score), white, 10, 'small', 120, 0)
    message_to_screen("Lives: " + str(lives), white, 10, 'small', 500, 0)
    pygame.display.update()
    pygame.time.Clock().tick(snake_speed)


pygame.quit()
quit()

