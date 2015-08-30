running the python/src/web/exchange/webqqModule/webMain/__init__.py

qq and password can change in __init__.py

还存在的问题：
1，输入命令之后要等待1秒才能返回，原因在使用POPEN的时候，使用回调进行发送消息，给1秒来装在回调内容，使用readline装载完成的时候会阻塞起来，无法知道何时装载完成
2，针对不同QQ用户没有处理
3，kill和terminate方法有问题