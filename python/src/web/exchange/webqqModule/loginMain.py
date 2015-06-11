__author__ = 'zhouyi1'
import checkAuthCode,getAuthCode,login1,urllib,loginSigGet
loginSigGet.coreGetLoginSig()
cj = checkAuthCode.checkIn()
getAuthCode.coreGetCode()
login1.login(cj)
# print urllib.unquote(r'http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10')