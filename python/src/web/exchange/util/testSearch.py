#coding=utf-8
__author__ = 'zhouyi1'

import re

html = r"ptuiCB('0','0','http://ptlogin4.web2.qq.com/check_sig?pttype=1&uin=2236678453&service=login&nodirect=0&ptsigx=a6963d28f20b4db5197573396c9b603a5c996a86650a39554abf3e81d63dd05c7bb21a49a03a6784f19f1e88182deb102f31cbbc7293042fa22720874fddc69f&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&f_url=&ptlang=2052&ptredirect=100&aid=501004106&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=1&pt_aid=0&pt_aaid=0&pt_light=0&pt_3rd_aid=0','0','登录成功！', 'JAVA机器人');"
loginPostUrlGroup = re.search("'(.+)','(.+)','(.+)','(.*)','(.+)'", html)
print loginPostUrlGroup.group(3)