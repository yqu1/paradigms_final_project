from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall

# Factory for the server (host)
class ServerConnFactory(Factory):
	# just save gamespace on init
	def __init__(self, gs):
		self.gs = gs

	# Save the connection and return it, passing the gamespace
	def buildProtocol(self, addr):
		self.addr = addr
		self.conn = ServerConnection(addr, self.gs)
		return self.conn

# Host connection
class ServerConnection(Protocol):
	# Save gamespace, address
	def __init__(self, addr, gs):
		self.addr = addr
		self.gs = gs

	# When connection is made, start the game, add the looping call
	# This ensures the game will run indefinitely (at least on twisted's end)
	def connectionMade(self):
		print "connection made"
		self.gs.start()
		lc = LoopingCall(self.gs.tick)
		lc.start(1/60)

	# Send the data to the gamespace
	def dataReceived(self, data):
		self.gs.writeData(data)

	# Send the data through the connection
	def send(self, data):
		self.transport.write(data)

	# Conection lost
	def connectionLost(self, reason):
		print "lost connection"

# Connection factory for the client
class ClientConnFactory(ClientFactory):
	# Just save the gs on init
	def __init__(self, gs):
		self.gs = gs

	# Save the connection, passing it the gs
	def buildProtocol(self, addr):
		self.addr = addr
		self.conn = ClientConnection(addr, self.gs)
		return self.conn

# Connection for the client
class ClientConnection(Protocol):
	# Save the addr, gs on init
	def __init__(self, addr, gs):
		self.addr = addr
		self.gs = gs

	# On connection, start the game, add the looping call
	# This ensures the game will run indefinitely (at least on twisted's end)
	def connectionMade(self):
		print "connection made"
		self.gs.start()
		lc = LoopingCall(self.gs.tick)
		lc.start(1/60)

	# When you get data, send it to the gamespace
	def dataReceived(self, data):
		self.gs.writeData(data)

	# Send data through the connection
	def send(self, data):
		self.transport.write(data)

	# connection lost
	def connectionLost(self, reason):
		print "lost connection"
