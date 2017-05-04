import pygame
import random, sys
from pygame.locals import *

from enemy import Enemy

class GameSpace:
    def main(self):
        pygame.init()
        self.width = 500
        self.height = 500
        self.size = [self.width, self.height]
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())

        self.enemy_list = pygame.sprite.Group()
        self.add_enemy_rate = 6
        self.enemy_count = 0

        self.clock = pygame.time.Clock()

        while 1:
            self.clock.tick(60)

            self.enemy_count +=1
            if self.enemy_count == self.add_enemy_rate:
                self.enemy_count = 0
                speed = random.randrange(1, 10)
                enemy = Enemy(gs, speed)
                enemy.rect.x = random.randrange(self.width)
                enemy.rect.y = 0

                self.enemy_list.add(enemy)

            self.enemy_list.update()
            self.enemy_list.draw(self.screen)
            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
