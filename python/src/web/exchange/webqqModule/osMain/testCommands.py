__author__ = 'zy-xx'
import commands,os,select
from subprocess import *

handle = open(r'\tmp.log','wb+')

p = Popen("bash",shell=True, bufsize = 0, stdin=PIPE, stdout=handle, stderr=PIPE)
#
# readable,writeable,exceptional = select.select(p.stdout,p.stdin,[])
# print readable
# print writeable
# print exceptional

p.stdin.write("pwd\n")
p.stdin.flush()
# handle.truncate()
# print handle.read()
p.stdin.write("cd /tmp\n")
p.stdin.flush()
# handle.truncate()
p.stdin.write("pwd\n")
p.stdin.flush()
# handle.truncate()

# status,output = commands.getstatusoutput("pwd")
# print status
# print output
