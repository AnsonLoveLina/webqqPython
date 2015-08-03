#coding=utf-8
__author__ = 'zhouyi1'
import sys
import os
import hashlib

from twisted.internet.protocol import ServerFactory, ProcessProtocol
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor, threads

class TailProtocol(ProcessProtocol):
    def __init__(self, write_callback):
        self.write = write_callback

    def outReceived(self, data):
        self.write("Begin lastlog\n")
        data = [line for line in data.split('\n') if not line.startswith('==')]
        for d in data:
            self.write(d + '\n')
        self.write("End lastlog\n")

    def processEnded(self, reason):
        if reason.value.exitCode != 0:
            log.msg(reason)

class CmdProtocol(LineReceiver):

    delimiter = '\n'

    def processCmd(self, line):
        if line.startswith('exit'):
            self.transport.loseConnection()
        else:
            tailProtocol = TailProtocol(self.transport.write)
            reactor.spawnProcess(tailProtocol, '/usr/bin/tail', args=['/usr/bin/tail', '-10', '/var/log/syslog'])

    def connectionMade(self):
        self.client_ip = self.transport.getPeer()[1]
        log.msg("Client connection from %s" % self.client_ip)
        if len(self.factory.clients) >= self.factory.clients_max:
            log.msg("Too many connections. bye !")
            self.client_ip = None
            self.transport.loseConnection()
        else:
            self.factory.clients.append(self.client_ip)

    def connectionLost(self, reason):
        log.msg('Lost client connection.  Reason: %s' % reason)
        if self.client_ip:
            self.factory.clients.remove(self.client_ip)

    def dataReceived(self, data):
        log.msg('dataCmd received from %s : %s' % (self.client_ip, data))
        self.processCmd(data)

    def lineReceived(self, line):
        log.msg('lineCmd received from %s : %s' % (self.client_ip, line))
        self.processCmd(line)

class MyFactory(ServerFactory):

    protocol = CmdProtocol

    def __init__(self, clients_max=10):
        self.clients_max = clients_max
        self.clients = []

log.startLogging(sys.stdout)
reactor.listenTCP(9999, MyFactory(2))
reactor.run()
