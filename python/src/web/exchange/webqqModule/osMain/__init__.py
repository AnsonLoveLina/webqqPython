#coding=utf-8
__author__ = 'zhouyi1'

import random,os,ConfigParser,subprocess,json,urllib

class cmdEntity:
    def __init__(self,command,uin,type='shell',titleName='osCmdTitle'+str(random.uniform(10,20)),others=''):
        self.uin = uin
        self.titleName = titleName
        self.command = command
        self.type = type
        self.others = others
        self.version = uin

    def clear(self):
        self.version = 0

    def getTitleName(self):
        return self.titleName

    def getCommand(self):
        return self.command

    def getType(self):
        return self.type

    def getOthers(self):
        return self.others

config = ConfigParser.ConfigParser()
path = os.path.split(os.path.realpath(__file__))[0] + '/cmdType.conf'
config.read(path)

def initFriendsDic(jsonFriends):
    global datas
    jsonLists = list()
    jsons = json.loads(jsonFriends)
    for i in range(len(jsons)):
        jsonLists.append(jsons[i]['uin'])
    datas={}.fromkeys(jsonLists,-1)

def coreWrite(cmd,p):
    if p!=None:
        p.stdin.write(cmd.command+"\n")
        while True:
            buff = p.stdout.readline()
            print buff
            # 如果当前经常还没退出，并且BUFF已经没东西了。那么就意味着指令的输出读完了
            if buff == '' and p.poll() != None:
                break

def osHandle(cmd):
    # cmdEval = config.get('cmdType',cmd.getType())
    # cmdEval = str(cmdEval).replace('s%',cmd.getCommand(),1)
    # eval(cmdEval)
    global  datas
    p=None
    if cmd.uin==0:
        p = subprocess.Popen("bash",shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        # 如果发送消息的不是好友那么不予处理
        p = datas.get(int(cmd.uin),None)
    coreWrite(cmd,p)

# initFriendsDic(r'[{"face":591,"flag":285737536,"nick":"灰灰","uin":4192527649},{"face":522,"flag":4719170,"nick":"阿毅","uin":551435889}]')

# osHandle(cmdEntity('dir','551435889'))

# a = json.loads('{"retcode":0,"result":[{"poll_type":"message","value":{"msg_id":9988,"from_uin":3439173636,"to_uin":2236678453,"msg_id2":641242,"msg_type":9,"reply_ip":176757009,"time":1436410616,"content":[["font",{"size":12,"color":"000000","style":[0,0,0],"name":"\u5B8B\u4F53"}],"ss "]}}]}')
# print type(a['result'][0]['value'])
uin = 1
print '{"to":'+uin+',"content":"'+content+'","face":534,"clientid":'+self.clientid+',"msg_id":68880001,"psessionid":"'+self.login2Result['result']['psessionid']+'"}'

# print urllib.urlencode({'r':'{"ptwebqq"}'})