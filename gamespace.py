import pygame
import random, sys
from pygame.locals import *

from enemy import Enemy
from player import Player

class GameSpace:
    def main(self):
        pygame.init()
        self.width = 1000
        self.height = 500
        self.size = [self.width, self.height]
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())

        self.player = Player(self)

        self.bullet_list = pygame.sprite.Group()
        
        self.enemy_list = pygame.sprite.Group()
        self.add_enemy_rate = 6
        self.enemy_count = 0

        self.clock = pygame.time.Clock()

        while 1:
            self.clock.tick(60)

            # Generate new enemies with random speed
            self.enemy_count +=1
            if self.enemy_count == self.add_enemy_rate:
                self.enemy_count = 0
                speed = random.randrange(1, 5)
                hp = random.randrange(1, 3)
                enemy = Enemy(self, speed, hp)
                enemy.rect.x = random.randrange(self.width)
                enemy.rect.y = 0
                self.enemy_list.add(enemy)

            # Handle events
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.player.move(event.key)
                elif event.type == MOUSEBUTTONDOWN:
                    self.player.fire = True
                elif event.type == MOUSEBUTTONUP:
                    self.player.fire = False
                elif event.type == QUIT:
                    pygame.display.quit()
                
            # Update game objects    
            self.enemy_list.update()
            #self.player.update()
            #self.bullet_list.update()

            # Display current state of game objects
            self.screen.fill(self.black)
            self.enemy_list.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
