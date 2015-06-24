__author__ = 'zhouyi1'
import PyV8

def hashJs(q,ptwebqq):
    encryptionJs = open('mq_comm.js')
    encryptionJsCode = encryptionJs.read()
    ctxt = PyV8.JSContext()
    ctxt.enter()
    jsCode = encryptionJsCode
    encryptionJsFun = ctxt.eval(jsCode)
    hashCode = encryptionJsFun.u(q,ptwebqq)
    return hashCode

def hash(q,ptwebqq):
    N=ptwebqq + "password error"
    T=""
    V=[]
    while(1):
        if(T.__sizeof__() <= N)