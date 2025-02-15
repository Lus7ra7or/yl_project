import os
import pygame
from tkinter import messagebox

pygame.init()

screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird")

white = (255, 255, 255)
black = (0, 0, 0)

bg_image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'bg.png'))
start_button = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'start.png'))
exit_button = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'exit.png')), start_button.get_size())
reset_button = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img', 'reset.png'))

font = pygame.font.Font(None, 24)

def start():
    os.system('FlappyBird.py')


def read_statistics():
    stats_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statistics.txt')
    default_statistics = ["Средняя дистанция: -", "Максимальная дистанция: -", "Суммарная дистанция: -", "Количество игр: -"]
    if not os.path.exists(stats_file_path):
        return default_statistics
    try:
        with open(stats_file_path, 'r+') as file:
            numbers = file.read().split()
            numbers[0] = str(int(numbers[2]) // int(numbers[3]))
            default_statistics[0] = default_statistics[0] + ' ' + str(int(numbers[2]) // int(numbers[3]))
            for i in range(1, len(numbers)):
                default_statistics[i] = default_statistics[i] + ' ' + str(numbers[i])
            file.seek(0)
            file.write('\n'.join(map(str, numbers)))
            file.truncate()
            return default_statistics
    except:
        return default_statistics

def reset_statistics():
    result = messagebox.askyesno("Сброс статистики", "Вы уверены, что хотите сбросить статистику?")
    if result:
        with open('statistics.txt', 'w') as file:
            file.write("0\n0\n0\n0")
        return ["Средняя дистанция: 0", "Максимальная дистанция: 0", "Суммарная дистанция: 0", "Количество игр: 0"]
    else:
        return read_statistics()

stats = read_statistics()
running = True
while running:
    screen.blit(bg_image, (0, 0))
    text_color = black
    stats = read_statistics()

    for i, stat in enumerate(stats):
        text_surface = font.render(stat, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 50 * (i + 1)))
        screen.blit(text_surface, text_rect)

    button_start_x = (screen_width // 2) - (start_button.get_width() // 2)
    button_start_y = (screen_height // 2) - (start_button.get_height() // 2)
    screen.blit(start_button, (button_start_x, button_start_y))

    button_reset_x = (screen_width // 2) - (reset_button.get_width() // 2)
    button_reset_y = (screen_height // 2) + 25
    screen.blit(reset_button, (button_reset_x, button_reset_y))

    button_exit_x = (screen_width // 2) - (exit_button.get_width() // 2)
    button_exit_y = (screen_height // 2) + 75
    screen.blit(exit_button, (button_exit_x, button_exit_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_start_x <= mouse_pos[0] <= button_start_x + start_button.get_width() and \
                    button_start_y <= mouse_pos[1] <= button_start_y + start_button.get_height():
                start()
            if button_reset_x <= mouse_pos[0] <= button_reset_x + reset_button.get_width() and \
                    button_reset_y <= mouse_pos[1] <= button_reset_y + reset_button.get_height():
                stats = reset_statistics()
            if button_exit_x <= mouse_pos[0] <= button_exit_x + exit_button.get_width() and \
                    button_exit_y <= mouse_pos[1] <= button_exit_y + exit_button.get_height():
                running = False

    pygame.display.flip()

pygame.quit()