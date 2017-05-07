# Player 2 Program

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import sys, os, pygame, math
from pygame.locals import *
from twisted.internet.task import LoopingCall


# Function that loads images
def load_image(name):
    image = pygame.image.load(name)
    image = image.convert()
    return image, image.get_rect()

# GAMESPACE
class GameSpace():
    def __init__(self, p2Con):
	# Add network connection
	self.p2Con = p2Con

	# Initialize window settings
	pygame.init()
	pygame.key.set_repeat(100, 30)
        pygame.display.set_caption('kNockDown: player2')
	self.back = 30, 144, 255
	self.size = self.width, self.height = 640, 480
	self.screen = pygame.display.set_mode(self.size)

	# Initialize game objects
	self.clock = pygame.time.Clock()
	self.background = Background(self)
	self.myAvatar = Avatar(self, 'images/greensquare.png', 10, 10)
        self.enemyAvatar = Avatar(self, 'images/globe.png', 10, 20)
	self.sprites = [self.enemyAvatar, self.myAvatar]
	self.allsprites = pygame.sprite.RenderPlain(self.sprites)

    def loop(self):
	for event in pygame.event.get():
	    if event.type == QUIT:
		pygame.quit()
		sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.MyAvatar.move(-5) #move left
                elif event.key == pygame.K_RIGHT:
                    self.MyAvatar.move(5) #move right
#                elif event.key == pygame.K_SPACE:
                    #fire
        for sprite in self.sprites:
            sprite.tick()

	# Update screen
#        self.background.update()
#        self.allsprites.update()
	self.screen.fill(self.back)
        self.screen.blit(self.background.image, self.background.rect)
	for i in self.sprites:
	    self.screen.blit(i.image, i.rect)
#        self.background.draw(self.screen)
#	self.allsprites.draw(self.screen)
	pygame.display.flip()

# BACKGROUND
class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
	pygame.sprite.Sprite.__init__(self)
	self.image, self.rect = load_image('images/booth.jpg') 
	self.rect.topleft = 0, 0
    def tick(self):
	i = 1

# AVATAR CLASS
class Avatar(pygame.sprite.Sprite):
    def __init__(self, gs, image, x, y):
	pygame.sprite.Sprite.__init__(self)
	self.image, self.rect = load_image(image)
	self.rect.topleft = x, y

    def move(self, distance):
        self.rect = self.rect.move(distance,0)
        #self.rect.x = self.rect.x + distance
        pygame.display.update(self.rect)

    def tick(self):
	i = 5


# PLAYER 2 CONNECTION
class PlayerConnection(Protocol):
    def connectionMade(self):
	# Create player connection
	print'player 2 connection made'
	game = GameSpace(p2Con.getConnection())
	lc = LoopingCall(game.loop)
	lc.start(1/60)

    def dataReceived(self, data):
	# server.py has sent data to player 1: update game
	print 'data received from player1: ', data

class PlayerConnectionFactory(ClientFactory):
    def __init__(self):
	self.p2Con = PlayerConnection()
	
    def getConnection(self):
	return self.p2Con

    def buildProtocol(self, addr):
	return self.p2Con


if __name__ == "__main__":
    p2Con = PlayerConnectionFactory()
    reactor.connectTCP("ash.campus.nd.edu", 40403, p2Con)
    reactor.run()

