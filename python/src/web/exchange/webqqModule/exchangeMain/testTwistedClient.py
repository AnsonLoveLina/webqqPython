__author__ = 'zhouyi1'
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientCreator

class Greeter(Protocol):
    def sendMessage(self, msg):
        self.transport.write("MESSAGE %s/n" % msg)

    def connectionMade(self):
        self.transport.write("Hello server, I am the client!/r/n")

c = ClientCreator(reactor, Greeter)
c.connectTCP("localhost", 9999)
reactor.run()