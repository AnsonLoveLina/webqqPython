running the python/src/web/exchange/webqqModule/webMain/__init__.py

qq and password can change in __init__.py

The problems：
1, Waiting for one second after entering the command, for the reason when using the POPEN, the readline will be blocked and can not know when the load is completed.
2, According to different QQ users without processing
3, The kill and the terminate method has a bug