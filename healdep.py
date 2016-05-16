#!/usr/bin/python
import sys
import subprocess
args = sys.argv[1:]
#print args
ret = subprocess.call(args)

i = len(args) - 1
deplocation = None
while (i >= 0):
	if args[i] == '-MF':
		deplocation = args[i+1]
		break
	i = i - 1
if deplocation is None:
	exit(0)
objdir = '/'.join(deplocation.split('/')[:-2]) + '/.obj/'
depfile = open(deplocation)
lines = depfile.readlines()
depfile.close()
if not lines[0].startswith(objdir):
	lines[0] = objdir + lines[0]

depfile = open(deplocation, 'w')
for line in lines:
	depfile.write(line)
depfile.close()
#subprocess.call(['head', "-n1", deplocation])
exit(ret)
