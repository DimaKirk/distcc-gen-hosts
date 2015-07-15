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

pump = False
for param in sys.argv:
	if param == "--pump":
		pump = True
		print("pump mode on")


workpath = os.path.dirname( sys.argv[0] )
if len(workpath) > 0:
	workpath = workpath + '/'
print('workpath=\'' + workpath + '\'')
exclude_hosts = []
if os.path.exists(workpath + "exclude.hosts"):
	for line in open(workpath + "exclude.hosts", "r").read().split("\n"):
		exclude_hosts.append(line)

hosts = []
for line in open(workpath + "cluster.hosts", "r").read().split("\n"):
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
