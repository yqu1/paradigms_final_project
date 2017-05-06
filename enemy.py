import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gs, speed, hp):
        
        pygame.sprite.Sprite.__init__(self)

        self.gs = gs

        if hp > 1:
            self.orig_image = pygame.image.load("assets/enemy1.png")
            scale = 0.20
        else:
            self.orig_image = pygame.image.load("assets/enemy2.png")
            scale = 0.10
            
        img_w,img_h = self.orig_image.get_size()
        self.image = pygame.transform.scale(self.orig_image, (int(img_w*scale), int(img_h*scale))) 
        self.rect = self.image.get_rect()

        self.speed = speed
        self.hp = hp

    def update(self):

        # Move enemy downwards
        self.rect.y += self.speed

        # Check to see if enemy is still within screen boundaries
        screen_w, screen_h = self.gs.screen.get_size()
        if self.rect.y > screen_h:
            self.gs.enemy_list.remove(self)

            
        '''    
        # Check to see if enemy has been hit
        for b in self.gs.bullet_list:
            col = pygame.sprite.collide_rect(b, self)
            if col == True:
                self.hp = self.hp - 1
                self.gs.bullet_list.remove(b)

        # Remove enemy from game if hit points has reached 0
        if self.hp == 0:
            self.gs.enemy_list.remove(self)
        '''
            
