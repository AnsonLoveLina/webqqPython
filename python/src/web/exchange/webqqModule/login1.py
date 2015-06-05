__author__ = 'zhouyi1'
import urllib2,urllib,qqUser,subprocess,os,PyV8,sys
from encryption import QQmd5
class v8Doc(PyV8.JSClass):
     def write(self, s):
         print s.decode('utf-8')
     def getElementById(self,s):
        return s

class Global(PyV8.JSClass):
     def __init__(self):
         self.document = v8Doc()
         self.g_appid = 501004106

glob = Global()


def login():
    #encode begin process code error
    reload(sys)
    sys.setdefaultencoding('utf8')
    #encode end
    url = 'https://ssl.ptlogin2.qq.com/login'
    # print urllib.urlencode({'verifycode':r'!SDF'})
    # print urllib.urlencode({'verifycode':qqUser.authCode1})
    md5Pwd = str(QQmd5().md5_2(qqUser.pwd, qqUser.authCode1, qqUser.authCode2))
    encryptionJs = open('../../../../../js/mq_comm.js')
    encryptionJsCode = encryptionJs.read()
    #achieve document in js
    ctxt = PyV8.JSContext(glob)
    ctxt.enter()
    encryptionJsFun = ctxt.eval(encryptionJsCode)
    # pwd_salt = encryptionJsFun.md5(qqUser.pwd);
    # print 'pwd_salt:',pwd_salt
    # print 'authCode1:',qqUser.authCode1
    #smartPwd = encryptionJsFun.getEncryption(r'xx198742@',r'\x00\x00\x00\x00\x85\x51\x01\x35',r'!CMN',1)
    smartPwd = encryptionJsFun.getEncryption(qqUser.pwd,qqUser.authCode2,qqUser.authCode1,1)
    print 'smartPwd:',smartPwd
    datas = {'u':qqUser.qq,
             'p':smartPwd,
             'verifycode':qqUser.authCode1,
             'webqq_type':10,
             'remember_uin':1,
             'login2qq':1,
             'aid':qqUser.appid,
             'u1':r'http://w.qq.com/proxy.html?login2qq=1&webqq_type=10',
             'h':1,
             'ptredirect':0,
             'ptlang':2052,
             'daid':164,
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
             'login_sig':qqUser.loginSig,
             'pt_randsalt':0,
             'pt_vcode_v1':0,
             # 'pt_uistyle':'5',
             'pt_verifysession_v1':qqUser.pt_verifysession_v1}
    params = urllib.urlencode(datas)
    print url + '?' + params
    req = urllib2.Request(url=url+'?'+params,headers={'Content-Type' : 'text/xml'})
    req.add_header('Referer','https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=5&mibao_css=m_webqq&appid=%s&enable_qlogin=0&no_verifyimg=1&s_url=http%%3A%%2F%%2Fweb2.qq.com%%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20140612002'%qqUser.appid)
    resp = urllib2.urlopen(req)
    print resp.read()