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
from gamespace import *
from gameMenu import *
import pickle

from game_objects import *

# Client & Host information
#change the client port when necessary
CLIENT_PORT = 40051

#change the host name when necessary
HOST = 'localhost'

# Function to end game
def end():
    pygame.display.quit()
    sys.exit()

# Function to read keyboard input
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

# Function to draw text on screen
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (250, 250, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Multiplayer Gamespace
class GameSpace_multi:

    def __init__(self):

        # Initialize pygame display
        pygame.init()
        self.width = 1000
        self.height = 500
        self.size = [self.width, self.height]
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface(self.screen.get_size())
        self.running = True

        # Establish connection with host
        self.cf = ClientConnFactory(self)   
        reactor.connectTCP(HOST, CLIENT_PORT, self.cf)
        reactor.run()

    def start(self):

        # Initialize game objects
        self.player = Player(self)
        self.player.rect.x = 500
        self.player.rect.y = 400

        self.teammate = Player(self)
        self.teammate.rect.x = 400
        self.teammate.rect.y = 400
        
        self.bullet_list = pygame.sprite.Group()
        self.bullet_count = 0
        self.add_bullet_rate = 20
        
        self.enemy_list = pygame.sprite.Group()
        self.add_enemy_rate = 6
        self.enemy_count = 0
        
        self.scoreFont=pygame.font.SysFont("arial,tahoma", 20, True, True)
        self.font = pygame.font.SysFont(None, 48)

    def tick(self):

        # Update game state
        state = {}
        events = pygame.event.get()
        keys_down = pygame.key.get_pressed()
        state['events'] = self.packageEvents(events)
        state['keys_down'] = keys_down
        state['pos'] = (self.player.rect.x, self.player.rect.y)
        state['hp'] = self.player.hp
        state['score'] = self.player.score

        # Send state information to host
        self.sendState(state)

        # Call event handler loop
        self.handleEvents(self.player, events, keys_down)

        if self.running == True:

            # Update game objects
            self.player.update()
            self.teammate.update()
            self.enemy_list.update()
            self.bullet_list.update()

            # End game if both player has been killed
            if self.player.hp <= 0 and self.teammate.hp <= 0:
                self.running = False

            # Update display screen
            self.screen.fill(self.black)
            self.enemy_list.draw(self.screen)
            self.bullet_list.draw(self.screen)
            if self.player.hp > 0:
                self.screen.blit(self.player.image, self.player.rect)
            if self.teammate.hp > 0:
                self.screen.blit(self.teammate.image, self.teammate.rect)
            drawText('Score: %s' % (self.player.score), self.scoreFont, self.screen, 0, 0)
            drawText('HP: %s' % (self.player.hp), self.scoreFont, self.screen, 0, 460)
            pygame.display.flip()

        else:

            # Update display screen to indicate game is over
            drawText('Your Score: %s' % (self.player.score), self.scoreFont, self.screen, (self.width / 3) - 100, (self.height / 3) + 150)
            drawText('Teammate Score: %s' % (self.teammate.score), self.scoreFont, self.screen, (self.width / 3) + 100, (self.height / 3) + 150)
            drawText('GAME OVER', self.font, self.screen, (self.width / 3), (self.height / 3))
            drawText('Press esc to quit...', self.font, self.screen, (self.width / 3) - 80, (self.height / 3) + 50)
            pygame.display.update()
            waitForPlayerToPressKey()

    def handleEvents(self, player, events, keys_down):

        # Handle player input
        for event in events:
            if event.type == QUIT:
                end()
            elif event.type == MOUSEBUTTONDOWN:
                player.fire = True
            elif event.type == MOUSEBUTTONUP:
                player.fire = False

        # Update player position
        self.player.move(keys_down)

    def packageEvents(self, events):

        # Package events to send to client
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

        # Send state information to client
        s = pickle.dumps(state)
        self.cf.conn.send(s)

    def handleRemoteEvents(self, player, events, keys_down):

        # Handle events from host's player
        for event in events:
            if event['type'] == 'quit':
                sys.exit()
            elif event['type'] == 'mousedown':
                player.fire = True
            elif event['type'] == 'mouseup':
                player.fire = False

        # Update position of player
        player.move(keys_down)

    def writeData(self, data):

        # Add updates from host to client gamespace
        self.teammate_state = pickle.loads(data)

        try:
            pos = self.teammate_state['pos']
            events = self.teammate_state['events']
            keys_down = self.teammate_state['keys_down']
            self.teammate.score = self.teammate_state['score']
            self.teammate.hp = self.teammate_state['hp']
            self.teammate.rect.x = pos[0]
            self.teammate.rect.y = pos[1]
            self.handleRemoteEvents(self.teammate, events, keys_down)
            
            if 'enemy' in self.teammate_state:
                e = self.teammate_state['enemy']
                enemy = Enemy(self, e['speed'], e['hp'])
                enemy.rect.x = e['pos'][0]
                enemy.rect.y = e['pos'][1]
                self.enemy_list.add(enemy)                
        except Exception as ex:
            pass



if __name__ == '__main__':
    
    screen = pygame.display.set_mode((640, 480), 0, 32)
    menu_items = ('Quit', 'Single Player','Multi Player')
    funcs = {'Quit': sys.exit,
             'Multi Player': GameSpace_multi,
             'Single Player': GameSpace
             }
 
    pygame.display.set_caption('Space Wars')
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()
