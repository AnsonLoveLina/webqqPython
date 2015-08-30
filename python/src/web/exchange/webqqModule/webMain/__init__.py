#coding=utf-8
__author__ = 'zhouyi1'


import urllib2
import re
import random
import cookielib
import types
import getpass
import time
import json
from encryption import QQmd5
from PIL import Image
import PyV8
import binascii
import util

import socket,Queue

import thread

import urllib


import sys
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor
from queueExec import *


class v8Doc(PyV8.JSClass):
    def write(self, s):
        print s.decode('utf-8')
    def getElementById(self,s):
        return s

class Global(PyV8.JSClass):
    def __init__(self):
        self.document = v8Doc()
        self.g_appid = 501004106
class webqq:
    def __init__(self, user, pwd,queue):
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cookies),
                )
        urllib2.install_opener(self.opener)
        self.queue = queue
        self.user = user
        self.pwd = pwd
        self.appid = "501004106"
        self.daid = '164'
        self.js_ver = "10113"
        self.loginSig = r'fQ7Mq3WdteRUxPsYHfBLrJSyop-BFUpxtrumX0j*IgjgKFJ7TcpaCGHkQMM7LASk'
        self.cap_cd = r'LTXa5y7uicPpkG_XJp11SMZCIi5hijbx'
        self.mycookie = ";"
        self.getloginSig()
        #self.clientid = "21485768"
        #self.clientid = "34592990"
        self.clientid = str(random.randint(10000000, 99999999))

    def getloginSig(self):
        datas = {'aid': self.daid,
                 'target':'self',
                 'style':'16',
                 'mibao_css':'m_webqq',
                 'appid':self.appid,
                 'enable_qlogin':'0',
                 'no_verifyimg': '1',
                 's_url': 'http://w.qq.com/proxy.html',
                 'f_url':'loginerroralert',
                 'strong_login':'1',
                 'login_state':'10',
                 't':'20131024001'}
        url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?' + urllib.urlencode(datas)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        for cookie in self.cookies:
            if cookie.name == 'pt_login_sig':
                self.loginSig = cookie.value


    def getSafeCode(self):
        param = {'pt_tea':'1',
                'uin': self.user,
                'appid':self.appid,
                'js_ver': self.js_ver,
                'js_type':'0',
                'login_sig': self.loginSig,
                'u1':'http://w.qq.com/proxy.html',
                'r':random.random()}
        datas = urllib.urlencode(param)
        url = 'https://ssl.ptlogin2.qq.com/check?'+datas
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        #self.mycookie += "confirmuin=" + self.user + ";"
        #req.add_header('Cookie', self.mycookie)
        response  = urllib2.urlopen(req)
        html = response.read()
        #cs = ['%s=%s' %  (c.name, c.value) for c in self.cookies]
        #self.mycookie += ";".join(cs)
        verifycode = re.search("'(.+)','(.+)','(.+)','(.*)','(.+)'", html)
        self.check = verifycode.group(1)
        self.verifycode1 = str(verifycode.group(2))
        self.verifycode2 = str(verifycode.group(3))
        if self.check == "1":
            datas = {'aid': self.appid,
                     'uin': self.user,
                     'cap_cd': self.cap_cd,
                     'r':random.random()}
            url = 'https://ssl.captcha.qq.com/getimage?' + urllib.urlencode(datas)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
            urllib2.install_opener(opener)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            self.fi = open("./authCodeImg/authCodeImage.jpg", "wb")
            while 1:
                c = response.read()
                if not c:
                    break
                else :self.fi.write(c)
            self.fi.close()
            im = Image.open('./authCodeImg/authCodeImage.jpg')
            im.show()
            self.verifycode1 = raw_input("verifer:")
            for cookie in self.cookies:
                if cookie.name == 'verifysession':
                    self.pt_verifysession_v1 = cookie.value
        else:
            self.pt_verifysession_v1 = verifycode.group(4)
        # print self.check, self.verifycode1, self.verifycode2

    def getPwd(self):
        # self.md5Pwd = str(QQmd5().md5_2(self.pwd, self.verifycode1, self.verifycode2))
        encryptionJs = open('mq_comm.js')
        encryptionJsCode = encryptionJs.read()
        #achieve document in js
        ctxt = PyV8.JSContext(Global())
        ctxt.enter()
        jsCode = encryptionJsCode
        jsCode = jsCode[:-90] + "function ss(){var p='"+self.pwd+"';var verifycode1='"+self.verifycode1+"';var verifycode2='"+self.verifycode2+"';" \
        "return getEncryption(p,verifycode2,verifycode1,0)}" \
        "return {ss:ss,getEncryption: getEncryption, getRSAEncryption: getRSAEncryption, md5: md5}}();"
        # print jsCode
        encryptionJsFun = ctxt.eval(jsCode)
        smartPwd = encryptionJsFun.ss()
        return smartPwd

    def login1(self):
        #cs = ['%s=%s' %  (c.name, c.value) for c in self.cookies]
        #self.mycookie += ";" "; ".join(cs)
        smartPwd = self.getPwd()

        # print "smartPwd:",smartPwd

        # print "loginSig:",self.loginSig
        datas = {'u':self.user,
                 'p':smartPwd,
                 'verifycode':self.verifycode1,
                 'webqq_type':10,
                 'remember_uin':1,
                 'login2qq':1,
                 'aid':self.appid,
                 'u1':r'http://w.qq.com/proxy.html?login2qq=1&webqq_type=10',
                 'h':1,
                 'ptredirect':0,
                 'ptlang':2052,
                 'daid':self.daid,
                 'from_ui':1,
                 'pttype':1,
                 'dumy':'',
                 'fp':'loginerroralert',
                 'action':'0-15-9632',
                 'mibao_css':'m_webqq',
                 't':1,
                 'g':1,
                 'js_type':0,
                 'js_ver':10113,
                 'login_sig':self.loginSig,
                 'pt_randsalt':0,
                 'pt_vcode_v1':0,
                 # 'pt_uistyle':'5',
                 'pt_verifysession_v1':self.pt_verifysession_v1}

        params = urllib.urlencode(datas)
        login_url = 'https://ssl.ptlogin2.qq.com/login' + '?' + params
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        req = urllib2.Request(login_url)
        req.add_header("Referer", "https://ui.ptlogin2.qq.com/cgi-bin/login?daid="+self.daid+"&target=self&style=16&mibao_css=m_webqq&appid="+self.appid+"&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001")

        #req.add_header("Cookie", self.mycookie)
        #self.opener.addheaders.append(("Cookie", self.mycookie))
        resp = urllib2.urlopen(req)
        login1Html = resp.read()
        print login1Html
        login2UrlGroup = re.search("'(.+)','(.+)','(.+)','(.*)','(.+)'",login1Html)
        self.login2Url = login2UrlGroup.group(3)
        for cookie in self.cookies:
            # print cookie
            if cookie.name == 'ptwebqq':
                self.ptwebqq = cookie.value
            elif cookie.name == 'clientid':
                self.clientid = cookie.value


    def loginSigCheck(self):
        # print self.login2Url
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        req = urllib2.Request(self.login2Url)
        resp = urllib2.urlopen(req)
        resp.read()

    def getvfwebqq(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        req = urllib2.Request('http://s.web2.qq.com/api/getvfwebqq?ptwebqq='+self.ptwebqq+'&clientid='+self.clientid+"&psessionid=&t=1434982612214")
        req.add_header("Referer","http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1")
        resp = urllib2.urlopen(req)
        self.vfwebqqResult = json.load(resp)

    def login2(self):
        self.loginSigCheck()
        self.getvfwebqq()
        # print 'ptwebqq:',self.ptwebqq
        # print 'clientid:',self.clientid
        # values = {
        #     'ptwebqq':self.ptwebqq,
        #     'clientid':int(self.clientid),
        #     'psessionid':'',
        #     'status':'online'
        # }
        url = 'http://d.web2.qq.com/channel/login2'
        headerUrl = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        datas = 'r=%7B%22ptwebqq%22%3A%22'+self.ptwebqq+'%22%2C%22clientid%22%3A'+self.clientid+'%2C%22psessionid%22%3A%22%22%2C%22status%22%3A%22online%22%7D'
        # print datas
        req = urllib2.Request(url,datas)
        req.add_header("Referer", headerUrl)
        req.add_header("Content-Type", 'application/x-www-form-urlencoded')
        resp = urllib2.urlopen(req)
        # resultJson = resp.read()
        # print resultJson
        self.login2Result = json.load(resp)

    def getFriends(self):
        url = 'http://s.web2.qq.com/api/get_user_friends2'
        headerUrl = 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        datas = 'r=%7B%22vfwebqq%22%3A%22'+self.vfwebqqResult['result']['vfwebqq']+'%22%2C%22hash%22%3A%22'+util.hash(self.user,self.ptwebqq)+'%22%7D'
        req = urllib2.Request(url,datas)
        req.add_header("Referer", headerUrl)
        resp = urllib2.urlopen(req)
        # print resp.read()
        self.friends = json.load(resp)

    def reciveMsg(self):
        # print self.cookies
        url = 'http://d.web2.qq.com/channel/poll2'
        headerUrl = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        datas = {'r':'{"ptwebqq":"'+self.ptwebqq+'","clientid":'+self.clientid+',"psessionid":"'+self.login2Result['result']['psessionid']+'","key":""}'}
        datas = urllib.urlencode(datas)
        req = urllib2.Request(url,datas)
        req.add_header("Referer", headerUrl)
        resp = urllib2.urlopen(req)
        # print resp.read()
        self.rMsg = json.load(resp)
        # the poll_type maybe notify or else
        if 'retcode' in self.rMsg.keys() and self.rMsg['retcode']==0 and self.rMsg['result'][0]['poll_type']=='message':
            print 'already get the cmd,send it now!'
            print self.rMsg
            content = self.getDictValue(self.rMsg['result'][0]['value'],'content')[1]
            from_uin = self.getDictValue(self.rMsg['result'][0]['value'],'from_uin')
            queue.put({"from_uin":from_uin,"content":content})
            # self.sendMsg(from_uin,self.getDefaultContentStyle(content+' is a good cmd!'))

    def getDictValue(self,jsonObj,key,default=None):
        if type(jsonObj) is not types.DictType:
            return default
        if key in jsonObj.keys():
            return jsonObj[key]
        else:
            return default

    def getDefaultContentStyle(self,content):
        print content
        return r'[\"'+str(content)+r'\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]'

    def sendMsg(self,uin,content):
        # print 'uin:'+str(uin)
        # print 'content:'+content
        content = str(content)
        url = 'http://d.web2.qq.com/channel/send_buddy_msg2'
        headerUrl = 'http://d.web2.qq.com/proxy.html?v=20130916001&callback=1&id=2'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(opener)
        datas = {'r':'{"to":'+str(uin)+',"content":"'+content+'","face":534,"clientid":'+str(self.clientid)+',"msg_id":68880001,"psessionid":"'+str(self.login2Result['result']['psessionid'])+'"}'}
        # print datas
        datas = urllib.urlencode(datas)
        req = urllib2.Request(url,datas)
        req.add_header("Referer", headerUrl)
        resp = urllib2.urlopen(req)
        respJson = json.load(resp)
        # print respJson
        if respJson['result'] == 'ok' and respJson['retcode']==0:
            print 'send success!'
        # print 'send it over!'

queue = Queue.Queue(maxsize=10)

user = '2236678453'
pwd = 'xx198742@'
qq = webqq(user, pwd,queue)


def startLoop(queue,qq):
    reactor.callWhenRunning(QueueExec(queue,qq,reactor).execQueueJob)
    reactor.run()


def main():
    log.startLogging(sys.stdout)
    global queue,qq

    qq.getSafeCode()
    qq.login1()
    qq.login2()
    print 'login success!'

    startLoop(queue,qq)



if __name__ == "__main__":
    main()




# 想了很多模式，还是决定自动LOOP公共QUEUE，暂时先放弃SOCKET链接驱动的模式
# class CmdProtocol(LineReceiver):
#
#     delimiter = '\n'
#
#     def connectionMade(self):
#         if 'host' in self.transport.getPeer().__dict__.keys():
#             self.client_ip = self.transport.getPeer().host
#         else:
#             self.client_ip = self.transport.getPeer()[1]
#         log.msg("Client connection from %s" % self.client_ip)
#         if len(self.factory.clients) >= self.factory.clients_max:
#             log.msg("Too many connections. bye !")
#             self.client_ip = None
#             self.transport.loseConnection()
#         else:
#             self.factory.clients.append(self.client_ip)
#
#     def connectionLost(self, reason):
#         log.msg('Lost client connection.  Reason: %s' % reason)
#         if self.client_ip:
#             self.factory.clients.remove(self.client_ip)
#
#     def dataReceived(self, data):
#         log.msg('dataCmd received from %s : %s' % (self.client_ip, data))
#         processCmd(data)
#
#     def lineReceived(self, line):
#         log.msg('lineCmd received from %s : %s' % (self.client_ip, line))
#         processCmd(line)
#
# class MyFactory(ServerFactory):
#
#     protocol = CmdProtocol
#
#     def __init__(self, clients_max=10):
#         self.clients_max = clients_max
#         self.clients = []
#
# def processCmd(data):
#     global queue,qq
#     cmd = queue.get()
#     qq.sendMsg(cmd)