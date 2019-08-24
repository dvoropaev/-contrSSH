install:
	cp ./honeypot.py /usr/bin/
	cp ./contrSSH /usr/bin/
	cp ./hydracall.py /usr/bin/
	mkdir /var/log/contrSSH
keygen:
	ssh-keygen -t rsa -f server.key
	mv ./server.key.pub /var/log/contrSSH/server.pub
	mv ./server.key /var/log/contrSSH/server.key
