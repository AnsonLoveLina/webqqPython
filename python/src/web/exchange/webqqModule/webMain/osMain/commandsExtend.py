#coding = utf-8
__author__ = 'zy-xx'
from subprocess import *
import time,thread

# the @abstractproperty will update before 2015-08-30
class CommondProcess:
    # default lineDivisor is 8
    def __init__(self,callBackList,queueExec):
        self.pope = Popen('bash',shell=True,stdin=PIPE,stdout=PIPE,universal_newlines=True)
        self.callBackList = callBackList
        self.queueExec = queueExec
        # self.qq = qq

    def callBackExecOutPut(self,from_uin):
        time.sleep(1)
        # print 'callBack Ready'
        self.queueExec.execOutPut(from_uin)
        # print 'callBack End'

    def write(self,cmd,from_uin):
        self.pope.stdin.write(cmd+" \n")
        self.pope.stdout.flush()
        running = True
        if Popen.poll(self.pope) is None:
            thread.start_new(self.callBackExecOutPut,(from_uin,))
            while True and running:
                outPutLine = self.pope.stdout.readline().strip('\n')
                self.addCallBackList(outPutLine)
                # print 'write:',self.callBackList
                if outPutLine == '':
                    running = False

    def outPut(self):
        # print 'outPut:',self.callBackList
        return self.callBackList

    def addCallBackList(self,outPutLine):
        self.callBackList.append(outPutLine)

    def clearPast(self):
        del self.callBackList[:]

    def kill(self):
        self.pope.kill()

    def terminate(self):
        self.pope.terminate()


# s = r'/Users/zy-xx/Documents/githubWorkspace/webqqPython/python/src/web/exchange/webqqModule/webMain\n'
# s.replace(r'\n',r'\\n')
# print s
# s = r'/Users/zy-xx/Documents/githubWorkspace/webqqPython/python/src/web/exchange/webqqModule/webMain\\n'
# print s
# pope = Popen('bash',shell=True,stdin=PIPE,stdout=PIPE,universal_newlines=True)
# pope.stdin.write('pwd \n')
# print Popen.poll(pope)
# pope.terminate()
# time.sleep(5)
# print Popen.poll(pope)
