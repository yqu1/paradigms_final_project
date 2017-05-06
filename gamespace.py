import pygame
import random, sys
from pygame.locals import *

from game_objects import *

def end():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    end()
                if event.key == K_RETURN:
                    return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (250, 250, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class GameSpace:
    def main(self):
        pygame.init()



        self.width = 1000
        self.height = 500
        self.size = [self.width, self.height]
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())

        self.player = Player(self, 1)
        self.player.rect.x = 500
        self.player.rect.y = 400

        self.bullet_list = pygame.sprite.Group()
        
        self.enemy_list = pygame.sprite.Group()
        self.add_enemy_rate = 6
        self.enemy_count = 0
        self.bullet_count = 0
        self.add_bullet_rate = 20
        self.totalScore = 0
        scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)

        # screen = pygame.display.set_mode([self.width,self.height])
        pygame.display.set_caption('Raiden Simulation Game Engine')

        # game resources setup
        font = pygame.font.SysFont(None, 48)
        #scoreFont=pygame.font.SysFont(["Arial","Tahoma","Times New Roman","Verdana"], 20, True, True)  #how the list should be formatted.
        scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)

        self.clock = pygame.time.Clock()

        drawText('RAIDEN', font, self.screen, (self.width / 3), (self.height / 3))
        drawText('Press enter to start...', font, self.screen, (self.width / 3) - 80, (self.height / 3) + 50)
        pygame.display.update()
        waitForPlayerToPressKey()

        while True:
            while True:
                
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
                        if event.key == pygame.K_ESCAPE:
                            drawText('Paused', font, self.screen, (self.width / 3), (self.height / 3))
                            drawText('Press enter to play again or esc to quit...', font, self.screen, (self.width / 3) - 80, (self.height / 3) + 50)
                            pygame.display.update()
                            waitForPlayerToPressKey()

                    elif event.type == MOUSEBUTTONDOWN:
                        self.player.fire = True
                    elif event.type == MOUSEBUTTONUP:
                        self.player.fire = False
                    elif event.type == QUIT:
                        pygame.display.quit()

                keys_down = pygame.key.get_pressed()
                self.player.move(keys_down)

                    
                # Update game objects    
                self.enemy_list.update()
                self.player.update()
                self.bullet_list.update()
                #self.bullet_list.update()
                if self.player.hp <= 0:
                    break;

                # Display current state of game objects
                self.screen.fill(self.black)
                self.enemy_list.draw(self.screen)
                self.bullet_list.draw(self.screen)
                self.screen.blit(self.player.image, self.player.rect)
                drawText('Score: %s' % (self.totalScore), scoreFont, self.screen, 0, 0)
                drawText('HP: %s' % (self.player.hp), scoreFont, self.screen, 0, 460)
                pygame.display.flip()
                self.clock.tick(60)

            drawText('Total Score: %s' % (self.totalScore), scoreFont, self.screen, (self.width / 3), (self.height / 3) + 100)
            drawText('GAME OVER', font, self.screen, (self.width / 3), (self.height / 3))
            drawText('Press enter to play again or esc to quit...', font, self.screen, (self.width / 3) - 80, (self.height / 3) + 50)
            pygame.display.update()
            waitForPlayerToPressKey()
            self.player = Player(self)
            self.player.rect.x = 500
            self.player.rect.y = 400

            self.bullet_list = pygame.sprite.Group()
            
            self.enemy_list = pygame.sprite.Group()
            self.add_enemy_rate = 30
            self.enemy_count = 0
            self.totalScore = 0




if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
