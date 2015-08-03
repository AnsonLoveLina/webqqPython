#coding=utf-8
__author__ = 'zhouyi1'
import socket
address = ('localhost',9999)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.send('hihi')
