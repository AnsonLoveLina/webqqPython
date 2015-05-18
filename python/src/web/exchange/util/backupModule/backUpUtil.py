# coding=gbk
__author__ = 'zhouyi1'
import time,zipfile,os,threading
usingComment = ''
sourcePaths = ''
targetPath = ''
def exit():
    time.sleep(10)
    global sourcePaths
    global targetPath
    backup2ZipCore(sourcePaths,targetPath)
    os.abort()

def backup2ZipCore(sourcePaths,targetPath):
    global usingComment
    targetFirstPath = os.sep + time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if not os.path.isdir(targetPath + os.sep + targetFirstPath) :
        os.makedirs(targetPath + os.sep + targetFirstPath)
    if len(usingComment) == 0:
        targetFileName = os.sep + time.strftime('%H：%M：%S',time.localtime(time.time()))+'.zip'
    else:
        targetFileName = os.sep + usingComment + time.strftime('%H：%M：%S',time.localtime(time.time()))+'.zip'
    f = zipfile.ZipFile(targetPath + targetFirstPath + targetFileName, 'w' ,zipfile.ZIP_DEFLATED)
    for sourcePath in sourcePaths:
        if os.path.isfile(sourcePath):
            f.write(sourcePath)
        else :
            for root, dirs, files in os.walk(sourcePath):
                for name in files:
                    f.write(os.path.join(root, name))
                if len(files) == 0:
                    f.write(root)
    f.close()

def backup2Zip(paraSourcePaths,paraTargetPath):
    global sourcePaths
    global targetPath
    sourcePaths=paraSourcePaths
    targetPath=paraTargetPath
    t = threading.Thread(target=exit)
    #设置为守护线程
    t.setDaemon(True)
    #开始线程
    t.start()
    global usingComment
    usingComment = raw_input("enter a comment with the (the program will abort after 10 seconds)"+"".join(sourcePaths)+":")
    backup2ZipCore(sourcePaths,targetPath)

#test
backup2Zip({'E:\pyWorkspace\src','E:\pyWorkspace\.idea'},'E:\pyWorkspace\zip')