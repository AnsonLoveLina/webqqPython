__author__ = 'zhouyi1'
import urllib2,urllib,qqUser,subprocess,os,PyV8
from encryption import QQmd5
def login():
    url = 'https://ssl.ptlogin2.qq.com/login'
    # print urllib.urlencode({'verifycode':r'!SDF'})
    # print urllib.urlencode({'verifycode':qqUser.authCode1})
    md5Pwd = str(QQmd5().md5_2(qqUser.pwd, qqUser.authCode1, qqUser.authCode2))
    encryptionJs = open('../../../../../js/Encryption.js')
    encryptionJsCode = encryptionJs.read()
    ctxt = PyV8.JSContext()
    ctxt.enter()
    encryptionJsFun = ctxt.eval(encryptionJsCode)
    smartPwd = encryptionJsFun.getEncryption(md5Pwd,qqUser.authCode2,qqUser.authCode1,1)
    print 'pwd:',smartPwd
    # perPwd = os.popen('perl ')
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
             'action':'0-20-40920',
             'mibao_css':'m_webqq',
             't':2,
             'g':1,
             'js_type':0,
             'js_ver':10113,
             'login_sig':r'r0fGXXLaa*r2ugEV8seve8hSVzhtHXCwQSuAvKBd3nnmvURNOwA6szgUQzhF-*28',
             'pt_randsalt':0,
             'pt_vcode_v1':0,
             # 'pt_uistyle':'5',
             'pt_verifysession_v1':qqUser.pt_verifysession_v1}
    params = urllib.urlencode(datas)
    # print url + '?' + params
    req = urllib2.Request(url+'?'+params)
    req.add_header('Referer','https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=5&mibao_css=m_webqq&appid=%s&enable_qlogin=0&no_verifyimg=1&s_url=http%%3A%%2F%%2Fweb2.qq.com%%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20140612002'%qqUser.appid)
    resp = urllib2.urlopen(req)
    print resp.read()