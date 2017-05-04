import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gs, speed):
        
        super().__init__()

        self.gs = gs
        
        self.orig_image = pygame.image.load("/home/remote/mwilli37/project/paradigms_final_project/assets/enemy1.png")
        self.image = self.orig_image
        self.rect = self.image.get_rect()

        self.speed = speed

    def update(self):

        self.rect.y += self.speed
