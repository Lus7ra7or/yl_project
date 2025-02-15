import pygame
from pygame.locals import *
import gameState

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, game_state, random_event):
        pygame.sprite.Sprite.__init__(self)
        self.game_state = game_state
        self.images = []
        self.index = 0
        self.counter = 0
        if not random_event:
            for num in range(1, 4):
                img = pygame.image.load(f'img/bird{num}.png')
                self.images.append(img)
        else:
            img = pygame.image.load(f'img/pipe_bird.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if self.game_state.flying and not self.game_state.pause_status:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not self.game_state.game_over and not self.game_state.pause_status:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            if not self.game_state.pause_status:
                self.image = pygame.transform.rotate(self.images[self.index], -90)