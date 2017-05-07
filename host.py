import pygame
import random, sys
from pygame.locals import *

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from connection import *

import pickle

from game_objects import *

CLIENT_PORT = 40051
HOST = 'localhost'

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
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 500
        self.size = [self.width, self.height]
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())
        self.running = True
        self.cf = ServerConnFactory(self)   
        reactor.listenTCP(CLIENT_PORT, self.cf)
        reactor.run()

    def start(self):
        print("start")
        self.player = Player(self, 1)
        self.player.rect.x = 400
        self.player.rect.y = 400

        self.teammate = Player(self, 2)
        self.teammate.rect.x = 500
        self.teammate.rect.y = 400

        self.bullet_list = pygame.sprite.Group()
        self.curEnemy = {}
        self.enemy_list = pygame.sprite.Group()
        self.enemy_state_list = []
        self.add_enemy_rate = 6
        self.enemy_count = 0
        self.bullet_count = 0
        self.add_bullet_rate = 20
        self.totalScore = 0
        self.scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)

        self.screen2 = pygame.display.set_mode([self.width,self.height])
        # pygame.display.set_caption('Raiden Simulation Game Engine')

        # # game resources setup
        self.font = pygame.font.SysFont(None, 48)
        #scoreFont=pygame.font.SysFont(["Arial","Tahoma","Times New Roman","Verdana"], 20, True, True)  #how the list should be formatted.
        # self.clock = pygame.time.Clock()

        # drawText('RAIDEN', font, screen, (self.width / 3), (self.height / 3))
        # drawText('Press enter to start...', font, screen, (self.width / 3) - 80, (self.height / 3) + 50)
        # pygame.display.update()
        # waitForPlayerToPressKey()

    def tick(self):
        state = {}
        events = pygame.event.get()
        keys_down = pygame.key.get_pressed()
        print(keys_down)
        state['events'] = self.packageEvents(events)
        state['keys_down'] = keys_down
        state['pos'] = (self.player.rect.x, self.player.rect.y)
        state['enemy'] = self.curEnemy
        self.sendState(state)
        self.handleEvents(self.player, events, keys_down)
        print("sent")
        if self.running == True:
            self.enemy_count +=1
            if self.enemy_count == self.add_enemy_rate:
                self.enemy_count = 0
                speed = random.randrange(1, 5)
                hp = random.randrange(1, 3)
                enemy = Enemy(self, speed, hp)
                enemy.rect.x = random.randrange(self.width)
                enemy.rect.y = 0
                self.enemy_list.add(enemy)
                enemy_state = {}
                enemy_state['hp'] = hp
                enemy_state['speed'] = speed
                enemy_state['pos'] = (enemy.rect.x, enemy.rect.y)
                self.curEnemy = enemy_state
                #self.enemy_state_list.append(enemy_state)
                #events = pygame.event.get()
                #keys_down = pygame.key.get_pressed()
                #state['events'] = self.packageEvents(events)
                #state['keys_down'] = keys_down
                #state['pos'] = (self.player.rect.x, self.player.rect.y)
                #state['enemy'] = enemy_state
                #self.sendState(state)


            self.player.update()
            self.teammate.update()
            self.enemy_list.update()
            self.bullet_list.update()

            if self.player.hp <= 0 or self.teammate.hp <= 0:
                self.running = False
            self.screen.fill(self.black)
            self.enemy_list.draw(self.screen)
            self.bullet_list.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.teammate.image, self.teammate.rect)
            drawText('Score: %s' % (self.totalScore), self.scoreFont, self.screen, 0, 0)
            drawText('HP: %s' % (self.player.hp), self.scoreFont, self.screen, 0, 460)
            print("asd")
            pygame.display.flip()
        else:
            drawText('Total Score: %s' % (self.totalScore), self.scoreFont, self.screen, (self.width / 3), (self.height / 3) + 100)
            drawText('Your Score: %s' % (self.player.score), self.scoreFont, self.screen, (self.width / 3) - 50, (self.height / 3) + 50)
            drawText('Teammate Score: %s' % (self.teammate.score), self.scoreFont, self.screen, (self.width / 3) + 50, (self.height / 3) + 50)
            drawText('GAME OVER', self.font, self.screen, (self.width / 3), (self.height / 3))
            drawText('Press esc to quit...', self.font, self.screen, (self.width / 3) - 80, (self.height / 3) + 50)
            pygame.display.update()

    def handleEvents(self, player, events, keys_down):
        for event in events:
            if event.type == QUIT:
                sys.exit()
                # if event.key == pygame.K_ESCAPE:
                #     drawText('Paused', font, screen, (self.width / 3), (self.height / 3))
                #     drawText('Press enter to play again or esc to quit...', font, screen, (self.width / 3) - 80, (self.height / 3) + 50)
                #     pygame.display.update()
                #     waitForPlayerToPressKey()

            elif event.type == MOUSEBUTTONDOWN:
                player.fire = True
            elif event.type == MOUSEBUTTONUP:
                player.fire = False


        self.player.move(keys_down)

    def packageEvents(self, events):
        event_list = []
        for event in events:
            ev = {}
            ev['type'] = ''
            if event.type == QUIT:
                ev['type']='quit'
            elif event.type == KEYUP:
                ev['type']='keyup'
                ev['key']=event.key
            elif event.type == KEYDOWN:
                ev['type']='keydown'
                ev['key']=event.key
            elif event.type == MOUSEBUTTONDOWN:
                ev['type']='mousedown'
            elif event.type == MOUSEBUTTONUP:
                ev['type']='mouseup'
            event_list.append(ev)
        return event_list

    def sendState(self, state):
        s = pickle.dumps(state)
        self.cf.conn.send(s)

    def handleRemoteEvents(self, player, events, keys_down):
        for event in events:
            if event['type'] == 'quit':
                sys.exit()
            elif event['type'] == 'mousedown':
                player.fire = True
            elif event['type'] == 'mouseup':
                player.fire = False

        player.move(keys_down)

    def addData(self, data):
        self.teammate_state = pickle.loads(data)
        try:
            pos = self.teammate_state['pos']
            events = self.teammate_state['events']
            keys_down = self.teammate_state['keys_down']
            self.teammate.rect.x = pos[0]
            self.teammate.rect.y = pos[1]
            self.handleRemoteEvents(self.teammate, events, keys_down)
        except Exception as ex:
            pass



    # def main(self):

    #     while True:
    #         while True:
                
    #             # Generate new enemies with random speed
    #             self.enemy_count +=1
    #             if self.enemy_count == self.add_enemy_rate:
    #                 self.enemy_count = 0
    #                 speed = random.randrange(1, 5)
    #                 hp = random.randrange(1, 3)
    #                 enemy = Enemy(self, speed, hp)
    #                 enemy.rect.x = random.randrange(self.width)
    #                 enemy.rect.y = 0
    #                 self.enemy_list.add(enemy)

    #             # Handle events
    #             for event in pygame.event.get():
    #                 if event.type == QUIT:
    #                     sys.exit()
    #                     # if event.key == pygame.K_ESCAPE:
    #                     #     drawText('Paused', font, screen, (self.width / 3), (self.height / 3))
    #                     #     drawText('Press enter to play again or esc to quit...', font, screen, (self.width / 3) - 80, (self.height / 3) + 50)
    #                     #     pygame.display.update()
    #                     #     waitForPlayerToPressKey()

    #                 elif event.type == MOUSEBUTTONDOWN:
    #                     self.player.fire = True
    #                 elif event.type == MOUSEBUTTONUP:
    #                     self.player.fire = False
    #                 elif event.type == QUIT:
    #                     pygame.display.quit()

    #             keys_down = pygame.key.get_pressed()
    #             self.player.move(keys_down)

                    
    #             # Update game objects    
    #             self.enemy_list.update()
    #             self.player.update()
    #             self.bullet_list.update()
    #             #self.bullet_list.update()
    #             if self.player.hp <= 0:
    #                 break;

    #             # Display current state of game objects
    #             self.screen.fill(self.black)
    #             self.enemy_list.draw(self.screen)
    #             self.bullet_list.draw(self.screen)
    #             self.screen.blit(self.player.image, self.player.rect)
    #             drawText('Score: %s' % (self.totalScore), scoreFont, screen, 0, 0)
    #             drawText('HP: %s' % (self.player.hp), scoreFont, screen, 0, 460)
    #             pygame.display.flip()
    #             self.clock.tick(60)

    #         drawText('Total Score: %s' % (self.totalScore), scoreFont, screen, (self.width / 3), (self.height / 3) + 100)
    #         drawText('GAME OVER', font, screen, (self.width / 3), (self.height / 3))
    #         drawText('Press enter to play again or esc to quit...', font, screen, (self.width / 3) - 80, (self.height / 3) + 50)
    #         pygame.display.update()
    #         waitForPlayerToPressKey()
    #         self.player = Player(self)
    #         self.player.rect.x = 500
    #         self.player.rect.y = 400

    #         self.bullet_list = pygame.sprite.Group()
            
    #         self.enemy_list = pygame.sprite.Group()
    #         self.add_enemy_rate = 30
    #         self.enemy_count = 0
    #         self.totalScore = 0




if __name__ == '__main__':
    gs = GameSpace()
