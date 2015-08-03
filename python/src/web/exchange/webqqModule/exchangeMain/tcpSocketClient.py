__author__ = 'zy-xx'
import socket

address = ('localhost', 9999)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.send('hihi')
s.close()
