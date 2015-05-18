__author__ = 'zhouyi1'
import urllib2,urllib, random,re,qqUser,cookielib
def checkIn():
        param = {'pt_tea':'1',
                'uin': qqUser.qq,
                'appid':qqUser.appid,
                'js_ver': qqUser.js_ver,
                'js_type':'0',
                'login_sig': qqUser.loginSig,
                'u1':'http%3A%2F%2Fw.qq.com%2Fproxy.html',
                'r':random.random()}
        datas = urllib.urlencode(param)
        #using GOT request method
        url = 'https://ssl.ptlogin2.qq.com/check?'+datas
        #print url
        #req = urllib2.Request(url,datas)
        # cj = cookielib.CookieJar()
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        # urllib2.install_opener(opener)
        # response = urllib2.urlopen(url)
        # for index,cookie in enumerate(cj):
        #         print '[',index,']',cookie
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        html = response.read()
        # print html
        autchCode = re.search("'(.+)','(.+)','(.+)','(.*)','(.+)'", html)
        qqUser.checkAuthCode = autchCode.group(1)
        qqUser.authCode1 = autchCode.group(2)
        qqUser.authCode2 = autchCode.group(3)
        qqUser.authCode3 = autchCode.group(4)
        qqUser.pt_verifysession_v1 = autchCode.group(4)