import pygame
import random,sys
from pygame.locals import *

import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):   
    def __init__(self, gs, x, y, player):
        
        pygame.sprite.Sprite.__init__(self)

        # Initialize bullet attributes
        self.bulletSpeed = 5
        self.image = pygame.Surface([2, 2])
        self.image.fill(( 255, 255, 255))
        self.gs = gs
        self.rect = self.image.get_rect()    
        self.rect.x = x
        self.rect.y = y  
        self.player = player # Player who shot the bullet (origin)
        
    def update(self):

        # Bullet moves upwards towards enemies until exceeds boundaries of screen
        self.rect.y -= self.bulletSpeed
        screen_w, screen_h = self.gs.screen.get_size()
        if self.rect.y < 0:
            self.gs.bullet_list.remove(self)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gs, speed, hp):
        
        pygame.sprite.Sprite.__init__(self)

        self.gs = gs

        if hp > 1:
            # Create large enemy
            self.orig_image = pygame.image.load("assets/enemy1.png")
            scale = 0.20           
        else:
            # Create small enemy
            self.orig_image = pygame.image.load("assets/enemy2.png")
            scale = 0.10

        # Initialize enemy attributes
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

        # Check to see if enemy has been hit by player bullet
        for bullet in self.gs.bullet_list:
            if pygame.sprite.collide_circle(self, bullet):
                self.hp -= 2
                self.gs.bullet_list.remove(bullet)
                self.killer = bullet.player

        # If enemy has been killed, remove from gamespace
        if self.hp <= 0:
            self.gs.enemy_list.remove(self)
            self.killer.score +=1

class Player(pygame.sprite.Sprite):
    def __init__(self, gs):
        
        pygame.sprite.Sprite.__init__(self)

        # Initialize player attributes
        image=pygame.image.load('assets/hero1.png')
        imageRect=image.get_rect()
        image = pygame.transform.scale(image, (imageRect.right//2, imageRect.bottom//2))
        image=image.convert()
        self.image = image
        self.rect = self.image.get_rect()
        self.fire = False
        self.gs = gs
        self.hp = 100
        self.score = 0

    def update(self):
        if self.hp <= 0: 
            return 

        # Check to see whether or not player has been hit by an enemy
        for enemy in self.gs.enemy_list:
            if pygame.sprite.collide_circle(self, enemy):
                self.hp -= 20
                self.gs.enemy_list.remove(enemy)

        # Check to see whether or not player is firing bullets
        if self.fire:
            bullet = Bullet(self.gs, self.rect.x + 36, self.rect.y, self)
            self.gs.bullet_list.add(bullet)

    def move(self, key):
        if self.hp <= 0: 
            return 

        # Move player based on key pressed
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
