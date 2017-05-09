import pygame
import random,sys
from pygame.locals import *

import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):   
    def __init__(self, gs, x, y, player):
        pygame.sprite.Sprite.__init__(self) 
        self.bulletSpeed = 5
        self.image = pygame.Surface([2, 2])
        self.image.fill(( 255, 255, 255))
        self.gs = gs
        self.rect = self.image.get_rect()    
        self.rect.x = x
        self.rect.y = y  
        self.player = player
    def update(self):
        self.rect.y -= self.bulletSpeed
        screen_w, screen_h = self.gs.screen.get_size()
        if self.rect.y < 0:
            self.gs.bullet_list.remove(self)

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
        self.killer = None

    def update(self):

        # Move enemy downwards
        self.rect.y += self.speed

        # Check to see if enemy is still within screen boundaries
        screen_w, screen_h = self.gs.screen.get_size()
        if self.rect.y > screen_h:
            self.gs.enemy_list.remove(self)

        for bullet in self.gs.bullet_list:
            if pygame.sprite.collide_circle(self, bullet):
                self.hp -= 2
                self.gs.bullet_list.remove(bullet)
                self.killer = bullet.player


        if self.hp <= 0:
            self.gs.enemy_list.remove(self)
            self.killer.score +=1
            
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
            


class Player(pygame.sprite.Sprite):
    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self)
        image=pygame.image.load('assets/hero1.png')
        imageRect=image.get_rect()
        image = pygame.transform.scale(image, (imageRect.right//2, imageRect.bottom//2))
        image=image.convert()
        self.image = image
        #self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.fire = False
        self.gs = gs
        self.hp = 1
        self.score = 0

    def update(self):
        for enemy in self.gs.enemy_list:
            if pygame.sprite.collide_circle(self, enemy):
                self.hp -= 100
                self.gs.enemy_list.remove(enemy)

        if self.fire:
            bullet = Bullet(self.gs, self.rect.x + 36, self.rect.y, self)
            self.gs.bullet_list.add(bullet)

    def move(self, key):
        if key[K_a]:
            if self.rect.x != 0:
                self.rect = self.rect.move(-5, 0)

        elif key[K_d]:
            if self.rect.x != 900:
                self.rect = self.rect.move(5, 0)

        elif key[K_s]:
            if self.rect.y != 420:
                self.rect = self.rect.move(0, 5)

        elif key[K_w]:
            if self.rect.y != 0:
                self.rect = self.rect.move(0, -5)
