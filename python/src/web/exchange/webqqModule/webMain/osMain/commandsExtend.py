#coding = utf-8
__author__ = 'zy-xx'
from subprocess import *

# the @abstractproperty will update before 2015-08-30
class CommondProcess:
    # default lineDivisor is 8
    def __init__(self,callBackList,outDivisor=8):
        self.pope = Popen('bash',shell=True,stdin=PIPE,stdout=PIPE,universal_newlines=True)
        self.callBackList = callBackList
        self.outDivisor = outDivisor
        # self.qq = qq

    def write(self,cmd):
        self.pope.stdin.write(cmd+" \n")
        self.pope.stdout.flush()
        while True:
            self.callBackList.append(self.pope.stdout.readline())

    def outPut(self):
        if len(self.callBackList)>self.outDivisor:
            return '\n'.join(self.callBackList)
        else:
            return None

    def kill(self):
        self.pope.kill()

    def terminate(self):
        self.pope.terminate()
