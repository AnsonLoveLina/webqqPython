__author__ = 'zhouyi1'
import urllib2,urllib, random,cookielib,re
import qqUser,login1,checkAuthCode
from PIL import Image


def coreGetLoginSig():
        #https://ssl.captcha.qq.com/getimage?aid=1003903&r=0.2744625671611856&uin=2236678453&cap_cd=LTXa5y7uicPpkG_XJp11SMZCIi5hijbx
        datas = {'aid': qqUser.daid,
                 'target':'self',
                 'style':'16',
                 'mibao_css':'m_webqq',
                 'appid':qqUser.appid,
                 'enable_qlogin':'0',
                 'no_verifyimg': '1',
                 's_url': 'http://w.qq.com/proxy.html',
                 'f_url':'loginerroralert',
                 'strong_login':'1',
                 'login_state':'10',
                 't':'20131024001'}
        url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?' + urllib.urlencode(datas)
        # req = urllib2.Request(url)
        # response = urllib2.urlopen(req)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        for cookie in enumerate(cj):
            if cookie[1].name == 'pt_login_sig':
                qqUser.loginSig = cookie[1].value
                # print qqUser.loginSig
            # pattern = re.compile('(\S*)verifysession=(\S*)\s(\S*)')
            # if pattern.match(cookie):
            #     qqUser.authCode3 = pattern.groups[2]
            #     qqUser.pt_verifysession_v1 = pattern.groups[2]

