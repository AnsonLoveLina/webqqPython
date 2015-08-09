__author__ = 'zy-xx'
class QueueExec(object):

    def __init__(self,queue,qq,reactor):
        self.queue = queue
        self.qq = qq
        self.reactor = reactor

    def execQueueJob(self):
        while True:
            if self.queue.qsize()>0:
                cmdAndUinDic = self.queue.get()
                self.qq.sendMsg(cmdAndUinDic['from_uin'],self.qq.getDefaultContentStyle(cmdAndUinDic['content']))
            else:
                break
        self.reactor.callLater(1, self.execQueueJob)