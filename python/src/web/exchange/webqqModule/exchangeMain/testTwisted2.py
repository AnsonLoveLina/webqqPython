__author__ = 'zy-xx'
from twisted.internet import reactor
class Countdown(object):
    counter = 5
    def count(self):
        print self.counter, '...'
        reactor.callLater(1, self.count)

reactor.callLater(1, Countdown().count)

print 'Start!'
reactor.run()
print 'Stop!'