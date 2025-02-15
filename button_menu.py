import pygame
from pygame.locals import *
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
class ButtonMenu():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if action:
            try:
                with open('main.py', 'r') as f:
                    code = f.read()
                exec(code)
            except:
                pass
        return action