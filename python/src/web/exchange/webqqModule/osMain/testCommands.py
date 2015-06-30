__author__ = 'zy-xx'
import commands,os
from subprocess import *

p = Popen("bash",shell=True, bufsize = 0, stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.stdin.write("pwd\n")
print p.stdout.readline()
p.stdin.write("cd /tmp\n")
p.stdin.write("pwd\n")
print p.stdout.readline()

# status,output = commands.getstatusoutput("cd /")
# print status
# print output

# print os.popen('ls').read()