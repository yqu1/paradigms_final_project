import pygame
import random,sys
from pygame.locals import *



class Player(pygame.sprite.Sprite):
	def __init__(self, width, height, gs):
		pygame.sprite.Sprite.__init__(self) 
		image=pygame.image.load('plane1.png')
		imageRect=image.get_rect()
		image = pygame.transform.scale(image, (imageRect.right//2, imageRect.bottom//2))
		image=image.convert()
		self.image = image
		self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.fire = False
        self.gs = gs
        self.hp = 1000

    def update(self, key):
    	for enemy in self.gs.enemies:
    		if pygame.sprite.collide_circle(self, enemy):
    			self.hitpoints -= 15
    			self.gs.bullets.remove(enemy)

    	if self.fire:
    		#create and append bullet
    	if key == 276:
            self.rect = self.rect.move(-5, 0)

        elif key == 275:
            self.rect = self.rect.move(5, 0)

        elif key == 274:
            self.rect = self.rect.move(0, 5)

        elif key == 273:
            self.rect = self.rect.move(0, -5)
