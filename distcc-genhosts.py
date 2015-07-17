#!/usr/bin/python
import socket
import os
import sys

def CheckDistccPort(host):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.5)
		s.connect((host, 3632))
		s.close()
                return True
        except:
                return False

pump = '--pump' in sys.argv
if pump:
	print("pump mode on")

workpath = os.path.dirname( sys.argv[0] )
print("workpath = '{}'".format(workpath))

try:
	exclude_hosts = [line.strip() for line in open(os.path.join(workpath, "exclude.hosts"))]
except IOError:
	exclude_hosts = []

hosts = []
for line in open(os.path.join(workpath, "cluster.hosts")):
	line = line.strip()
	if len(line) < 1:
		continue
	host = line.split('/')[0]
	if host in exclude_hosts:
		print('exclude host ' + host)
		continue
	connect = CheckDistccPort(host)
	print(line + ' ' + str(connect))
	if connect:
		if pump:
			line = line + ',cpp'
		hosts.append(line + ',lzo')
hosts.append("\n")
open('/etc/distcc/hosts', 'w').write(' '.join(hosts))
