__author__ = 'zhouyi1'
import PyV8
encryptionJs = open('../../../../../js/Encryption.js')
encryptionJsCode = encryptionJs.read()
ctxt = PyV8.JSContext()
ctxt.enter()
func = ctxt.eval(encryptionJsCode)
print func.getEncryption("2954c637de599a43c8584205923f68b1","\x00\x00\x00\x00\xb7\x23\xc2\x72","netx",1)
