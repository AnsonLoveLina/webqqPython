#coding=utf-8
__author__ = 'zhouyi1'
import Queue
import threading,random
from osCore import cmdEntity

#目前打算用事件驱动模型处理

# 之后将换成PriorityQueue优先级队列，保证一些人的命令是比较先处理，但是由于目前没想好优先的规则，暂时就不弄了
queue = Queue.Queue()

class cmdProducer(threading.Thread):
    def __init__(self,cmd,queue):
        threading.Thread.__init__(self, name=cmd.getTitleName('titleName')+str(random.randint(1,99)))
        self.cmdQueue = queue
        self.cmd = cmd

    def run(self):
        self.cmdQueue.put(self.cmd.getCommand('command'),1)
        print 'command:s% is put in the queue!'%(self.cmd.getCommand('titleName'))

class cmdHandler(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self, name=str(random.randint(1,queue.qsize())))
        self.cmdQueue = queue

    def run(self):
        # if not self.cmdQueue.empty():
            # 如果拿不到那么就阻塞着
            cmd = self.cmdQueue.get(True)
            print 'execting s%',cmd

def main():
    p = cmdProducer(cmdEntity('dir'),queue)
    p.start()
    c = cmdHandler(queue)
    c.start()

if __name__ == '__main__':
    main()
