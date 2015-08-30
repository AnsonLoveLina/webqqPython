#coding = utf-8
__author__ = 'zy-xx'
from subprocess import *

# the @abstractproperty will update before 2015-08-30
class CommondProcess:
    # default lineDivisor is 8
    def __init__(self,callBackList):
        self.pope = Popen('bash',shell=True,stdin=PIPE,stdout=PIPE,universal_newlines=True)
        self.callBackList = callBackList
        # self.qq = qq

    def write(self,cmd):
        self.pope.stdin.write(cmd+" \n")
        self.pope.stdout.flush()
        running = True
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
# # print pope.wait()
# pope.stdin.write('pwd \n')
# pope.stdout.flush()
# print pope.stdout.read()
