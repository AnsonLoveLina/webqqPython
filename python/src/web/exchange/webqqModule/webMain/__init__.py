#coding=utf-8
__author__ = 'zhouyi1'


import urllib2
import re
import random
from encryption import QQmd5
import cookielib
import getpass
import time
import json
from PIL import Image
import PyV8
import binascii

import urllib



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
    def __init__(self, user, pwd):
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cookies),
                )
        urllib2.install_opener(self.opener)
        self.user = user
        self.pwd = pwd
        self.appid = "501004106"
        self.daid = '164'
        self.js_ver = "10113"
        self.loginSig = r'fQ7Mq3WdteRUxPsYHfBLrJSyop-BFUpxtrumX0j*IgjgKFJ7TcpaCGHkQMM7LASk'
        self.cap_cd = r'LTXa5y7uicPpkG_XJp11SMZCIi5hijbx'
        self.mycookie = ";"
        #self.clientid = "21485768"
        #self.clientid = "34592990"
        self.clientid = str(random.randint(10000000, 99999999))

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
                    self.pt_verifysession_v1 = self.cookies
        else:
            self.pt_verifysession_v1 = verifycode.group(4)
        print self.check, self.verifycode1, self.verifycode2

    def getPwd(self):
        md5Pwd = str(QQmd5().md5_2(self.pwd, self.verifycode1, binascii.b2a_hex(self.verifycode2)))
        encryptionJs = open('mq_comm.js')
        encryptionJsCode = encryptionJs.read()
        #achieve document in js
        ctxt = PyV8.JSContext(Global())
        ctxt.enter()
        jsCode = encryptionJsCode[:-90] + " function ss(){var p = '"+self.pwd+"';var salt = '"+self.verifycode1+"';var verifycode = '"+self.verifycode2+"';var r = $.Encryption.getEncryption(p,salt,verifycode,0);return (r);} " \
                                                                                                                                                        "return {ss: ss,getEncryption: getEncryption, getRSAEncryption: getRSAEncryption, md5: md5}}();"
        encryptionJsFun = ctxt.eval(jsCode)
        smartPwd = encryptionJsFun.ss()
        return smartPwd

    def loginGet(self):
        #cs = ['%s=%s' %  (c.name, c.value) for c in self.cookies]
        #self.mycookie += ";" "; ".join(cs)
        smartPwd = str(self.getPwd())

        print smartPwd

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
                 'login_sig':'',
                 'pt_randsalt':0,
                 'pt_vcode_v1':0,
                 # 'pt_uistyle':'5',
                 'pt_verifysession_v1':self.pt_verifysession_v1}

        params = urllib.urlencode(datas)
        login_url = 'https://ssl.ptlogin2.qq.com/login' + '?' + params
        req = urllib2.Request(login_url)
        req.add_header("Referer", "https://ui.ptlogin2.qq.com/cgi-bin/login?daid="+self.daid+"&target=self&style=16&mibao_css=m_webqq&appid="+self.appid+"&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001")

        #req.add_header("Cookie", self.mycookie)
        #self.opener.addheaders.append(("Cookie", self.mycookie))
        resp = urllib2.urlopen(req)
        print resp.read()
        for cookie in self.cookies:
            print cookie
        #
        # print urllib2.urlopen('http://web2.qq.com/web2/get_msg_tip?uin=&tp=1&id=0&retype=1&rc=0&lv=3&t=1358252543124').read()
        # #cs = ['%s=%s' %  (c.name, c.value) for c in self.cookies]
        # #self.mycookie += ";" "; ".join(cs)



def main():
    user = '2236678453'
    pwd = 'xx198742@'
    qq = webqq(user, pwd)
    qq.getSafeCode()
    qq.loginGet()
    # qq.loginPost()
    # qq.getGroupList()
    # qq.getFriend()


if __name__ == "__main__":
    main()