import pygame
import math
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, gs):

        super().__init__()

        self.gs = gs
        self.orig_image = pygame.image.load("/home/remote/mwilli37/project/paradigms_final_project/assets/hero1.png")
        img_w,img_h = self.orig_image.get_size()
        scale = 0.20
        self.image = pygame.transform.scale(self.orig_image, (int(img_w*scale), int(img_h*scale)))
        self.rect = self.image.get_rect()
        screen_w,screen_h = self.gs.screen.get_size()
        self.rect.x = 0.5*screen_w
        self.rect.y = screen_h - (int(img_h*scale)) + 1

    def move(self, direction):

        if direction == K_DOWN:
            self.rect.y = self.rect.y + 10
        elif direction == K_UP:
            self.rect.y = self.rect.y - 10
        elif direction == K_RIGHT:
            self.rect.x = self.rect.x + 10
        elif direction == K_LEFT:
            self.rect.x = self.rect.x - 10
            
    def tick(self):
        #Check for mouse location
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        angle = 360 - math.degrees(math.atan2(self.rect.centery - mouse_y, self.rect.centerx - mouse_x)) + 135
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
