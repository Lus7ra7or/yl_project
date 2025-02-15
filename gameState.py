import pygame
from pygame.locals import *

class GameState:
    def __init__(self):
        self.ground_scroll = 0
        self.scroll_speed = 4
        self.flying = False
        self.game_over = False
        self.pipe_gap = 300
        self.pipe_frequency = 1500
        self.show_start_message = True
        self.pause_status = False
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
        self.score = 0
        self.pass_pipe = False
        self.random_event = True

    def reset(self):
        self.score = 0
        self.flying = False
        self.game_over = False
        self.pause_status = False
        self.ground_scroll = 0
        self.show_start_message = True
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency