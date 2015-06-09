__author__ = 'zhouyi1'
import urllib2,urllib, random,cookielib,re
import qqUser,login1,checkAuthCode
from PIL import Image
def coreGetCode():
    #'1' ment need authCode
    if qqUser.checkAuthCode=='1':
        #https://ssl.captcha.qq.com/getimage?aid=1003903&r=0.2744625671611856&uin=2236678453&cap_cd=LTXa5y7uicPpkG_XJp11SMZCIi5hijbx
        datas = {'aid': qqUser.appid,
                 'uin': qqUser.qq,
                 'cap_cd': qqUser.cap_cd,
                 'r':random.random()}
        url = 'https://ssl.captcha.qq.com/getimage?' + urllib.urlencode(datas)
        cj = qqUser.cj
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        qqUser.cj = cj
        for cookie in enumerate(cj):
            print cookie
        fl = open('./authCodeImg/authCodeImage.jpg','wb')
        while 1:
            c = response.read()
            if not c:
                break
            else:
                fl.write(c)
        fl.close()
        im = Image.open('./authCodeImg/authCodeImage.jpg')
        im.show()
        qqUser.authCode1 = raw_input('authCode:')