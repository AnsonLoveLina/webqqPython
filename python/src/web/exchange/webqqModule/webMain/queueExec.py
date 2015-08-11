__author__ = 'zy-xx'
import thread,time
class QueueExec(object):

    def __init__(self,queue,qq,reactor):
        self.queue = queue
        self.qq = qq
        self.reactor = reactor

    def execQueueJob(self):
        self.qq.reciveMsg()
        while True:
            if self.queue.qsize()>0:
                cmdAndUinDic = self.queue.get()
                self.qq.sendMsg(cmdAndUinDic['from_uin'],self.qq.getDefaultContentStyle(self.execCmd(cmdAndUinDic)))
            else:
                break
        self.reactor.callLater(1, self.execQueueJob)
        time.sleep(5)

    # we need from_uin and the 'break' cmd to decide about the cmd thread
    def execCmd(self,cmdAndUinDic):
        return cmdAndUinDic['content'],' is the good cmd!'