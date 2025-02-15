import pygame
from pygame.locals import *
import random
import gameState
import bird
import button
import pipe
import button_menu
import sys
import os

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 836

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')
button_img_exit = pygame.image.load('img/exit.png')
stats_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statistics.txt')

font = pygame.font.SysFont('Bauhaus 93', 60)

white = (255, 255, 255)
dark_blue = (0, 0, 102)

game_state = gameState.GameState()

game_state.pause_status = False

def update_statistics_games():
    with open('statistics.txt', 'r+') as file:
        numbers = file.read().split()
        new_numbers = [int(i) for i in numbers]
        new_numbers[3] += 1
        file.seek(0)
        file.write('\n'.join(map(str, new_numbers)))
        file.truncate()


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

game_state.random_event = random.random() < 0.25

flappy = bird.Bird(100, int(screen_height / 2), game_state, game_state.random_event)
bird_group.add(flappy)
button = button.Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)
button_exit = button_menu.ButtonMenu(screen_width // 2 - 50, screen_height // 2 - 50, button_img_exit)
update_statistics_games()
run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (game_state.ground_scroll, 768))

    if len(pipe_group) > 0:
        bird = bird_group.sprites()[0]
        first_pipe = pipe_group.sprites()[0]
        if bird.rect.left > first_pipe.rect.left and bird.rect.right < first_pipe.rect.right and not game_state.pass_pipe:
            game_state.pass_pipe = True
        if game_state.pass_pipe and bird.rect.left > first_pipe.rect.right:
            with open('statistics.txt', 'r+') as file:
                numbers = file.read().split()
                new_numbers = [int(i) for i in numbers]
                new_numbers[2] += 1
                if game_state.score > new_numbers[1]:
                    new_numbers[1] = game_state.score
                file.seek(0)
                file.write('\n'.join(map(str, new_numbers)))
                file.truncate()
            game_state.score += 1
            game_state.pass_pipe = False


    draw_text(str(game_state.score), font, white, int(screen_width / 2), 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_state.game_over = True

    if flappy.rect.bottom >= 768:
        game_state.game_over = True
        game_state.flying = False

    if not game_state.game_over and game_state.flying and not game_state.pause_status:
        time_now = pygame.time.get_ticks()
        if time_now - game_state.last_pipe > game_state.pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, game_state, game_state.random_event)
            top_pipe = pipe.Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, game_state, game_state.random_event)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            game_state.last_pipe = time_now

        game_state.ground_scroll -= game_state.scroll_speed
        if abs(game_state.ground_scroll) > 35:
            game_state.ground_scroll = 0
        pipe_group.update()
    elif game_state.pause_status:
        draw_text("Paused", font, white, int(screen_width / 2), screen_height // 4)
        if button.draw():
            game_state.reset()
            pipe_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            update_statistics_games()
        if button_exit.draw():
            pygame.quit()
            sys.exit()

    if game_state.game_over:
        if button.draw():
            game_state.reset()
            pipe_group.empty()
            flappy.rect.x = 100
            flappy.rect.y = int(screen_height / 2)
            update_statistics_games()
        if button_exit.draw():
            pygame.quit()
            sys.exit()
    if game_state.show_start_message:
        draw_text("Click to Start", font, dark_blue, screen_width // 2 - 120, screen_height // 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not game_state.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if not game_state.pause_status:
                        game_state.pause_status = True
                    else:
                        game_state.pause_status = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_state.flying and not game_state.game_over and not game_state.pause_status:
            game_state.flying = True
            game_state.show_start_message = False

    pygame.display.update()
pygame.quit()
sys.exit()