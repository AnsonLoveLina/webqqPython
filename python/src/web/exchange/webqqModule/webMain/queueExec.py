__author__ = 'zy-xx'
import thread,time
from osMain.commandsExtend import *
class QueueExec(object):

    def __init__(self,queue,qq,reactor,outDivisor=8):
        self.queue = queue
        self.qq = qq
        self.reactor = reactor
        self.commondProcess = CommondProcess([])
        self.breakCmd = {'kill':self.commondProcess.kill,'terminate':self.commondProcess.terminate}
        self.outDivisor = outDivisor

    def execQueueJob(self):
        # recive the msg everytime and exec the queue's content from the execCmd,
        # finally callLater about the next loop and sleep 5 seconds
        self.qq.reciveMsg()
        # print 'recived'
        while True:
            if self.queue.qsize()>0:
                cmdAndUinDic = self.queue.get()
                resultList = self.execCmd(cmdAndUinDic)
                # avoid a large number of return
                for result in resultList:
                    self.qq.sendMsg(cmdAndUinDic['from_uin'],self.qq.getDefaultContentStyle(result))
                # clear the past result
                self.commondProcess.clearPast()
            else:
                break
        self.reactor.callLater(1, self.execQueueJob)
        time.sleep(5)

    # we need from_uin and the 'kill' or 'terminate' cmd to decide about the cmd thread
    def execCmd(self,cmdAndUinDic):
        if str(cmdAndUinDic['content']) in self.breakCmd.keys():
            self.breakCmd[str(cmdAndUinDic['content'])]
        else:
            thread.start_new(self.commondProcess.write,(cmdAndUinDic['content'],))
        # the time.sleep is the bad code
        time.sleep(5)
        sourceList = self.commondProcess.outPut()

        # paging though the outDivisor
        outPutList = []
        begin = 0
        while not len(sourceList) < begin:
            outPutList.append(sourceList[begin:begin+self.outDivisor])
            begin += self.outDivisor
        return outPutList