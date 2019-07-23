#!/usr/bin/python
import socket
import os
import sys

def CheckDistccPort(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.5)
		s.connect((host, port))
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
filename = "cluster.hosts"
if "--file" in sys.argv:
	filename = sys.argv[sys.argv.index("--file") + 1]
	
for line in open(os.path.join(workpath, filename)):
	line = line.strip()
	if len(line) < 1:
		continue
	port = 3632
	host = line.split('/')[0]
	if ":" in host:
		port = int(host .split(':')[1])
		host = host .split(':')[0]
	if host in exclude_hosts:
		print('exclude host ' + host)
		continue
	connect = CheckDistccPort(host, port)
	print(line + ' ' + str(connect))
	if connect:
		if pump:
			line = line + ',cpp'
		hosts.append(line + ',lzo')
hosts.append("\n")
open('/etc/distcc/hosts', 'w').write(' '.join(hosts))
