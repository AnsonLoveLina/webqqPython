__author__ = 'zhouyi1'
import urllib2,urllib,qqUser
url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=5&mibao_css=m_webqq&appid=%s&enable_qlogin=0&no_verifyimg=1&s_url=http%%3A%%2F%%2Fweb2.qq.com%%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20150209002'%qqUser.appid
req = urllib2.Request(url)
response = urllib2.urlopen(req)
html = response.read()
print html