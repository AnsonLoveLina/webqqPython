__author__ = 'zy-xx'
import thread,time
from osMain.commandsExtend import *
class QueueExec(object):

    def __init__(self,queue,qq,reactor):
        self.queue = queue
        self.qq = qq
        self.reactor = reactor
        self.commondProcess = CommondProcess([])

    def execQueueJob(self):
        # recive the msg everytime and exec the queue's content from the execCmd,
        # finally callLater about the next loop and sleep 5 seconds
        self.qq.reciveMsg()
        while True:
            if self.queue.qsize()>0:
                cmdAndUinDic = self.queue.get()
                resultList = self.execCmd(cmdAndUinDic)
                # avoid a large number of return
                for result in resultList:
                    self.qq.sendMsg(cmdAndUinDic['from_uin'],self.qq.getDefaultContentStyle(result))
            else:
                break
        self.reactor.callLater(1, self.execQueueJob)
        time.sleep(5)

    # we need from_uin and the 'kill' or 'terminate' cmd to decide about the cmd thread
    def execCmd(self,cmdAndUinDic):
        thread.start_new(self.commondProcess.write,cmdAndUinDic['content'])
        return self.commondProcess.outPut()