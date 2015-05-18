__author__ = 'zhouyi1'
import urllib2,urllib,qqUser,cookielib
def initQQUser():
        param = {'webqq_type':10,
                'remember_uin': 1,
                'login2qq':1,
                'u1':'http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10',
                'aid':qqUser.appid,
                'ptredirect':0,
                'ptlang':2052,
                'daid':164,
                'from_ui':1,
                'pttype':1,
                'fp':'loginerroralert',
                'action':'0-15-26373',
                'mibao_css':'m_webqq',
                't':1,
                'g':1,
                'js_type':0,
                'js_ver':qqUser.js_ver,
                'pt_randsalt':0}
        datas = urllib.urlencode(param)
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'+datas
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        for index,cookie in enumerate(cj):
                print '[',index,']',cookie
        # req = urllib2.Request(url)
        # response = urllib2.urlopen(req)
initQQUser()