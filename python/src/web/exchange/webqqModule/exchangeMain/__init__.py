#coding=utf-8
__author__ = 'zhouyi1'
class a:
    x=1
print "true" if 'x' in a.__dict__.keys() else "false"