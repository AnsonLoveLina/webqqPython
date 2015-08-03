#coding=utf-8
__author__ = 'zhouyi1'
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
class MessageSend(Protocol):
    def connectionMade(self):
        # 连接上服务器后，打印出欢迎信息
        self.transport.write("Hello Server,I am the client\n")
    def sendMessage(self,msg):
        # 发送一条消息
        self.transport.write("MESSAGE:%s\n" % msg)

def gotProtocol(p):
    p.sendMessage("Hello server")
    # 添加两个延迟函数，分别在1秒之后，两秒之后运行。
    reactor.callLater(1,p.sendMessage,"This is send in a second")
    reactor.callLater(2,p.transport.loseConnection)

c = ClientCreator(reactor,MessageSend)
c.connectTCP("localhost",9999).addCallback(gotProtocol)
reactor.run()