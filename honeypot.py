#!/usr/bin/env python2.7
import socket, sys, threading, thread
import paramiko

#generate keys with 'ssh-keygen -t rsa -f server.key'
HOST_KEY = paramiko.RSAKey(filename='/var/log/contrSSH/server.key')
SSH_PORT = 22
LOGFILE = '/var/log/contrSSH/logins.log' #File to log the user:password combinations to
LOGFILE_LOCK = threading.Lock()

class SSHServerHandler (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        LOGFILE_LOCK.acquire()
        try:
            logfile_handle = open(LOGFILE,"a")
            print("New login: " + username + ":" + password)
            logfile_handle.write(username + ":" + password + "\n")
            logfile_handle.close()
        finally:
            LOGFILE_LOCK.release()
        return paramiko.AUTH_FAILED


    def get_allowed_auths(self, username):
        return 'password'

def handleConnection(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server_handler = SSHServerHandler()

    transport.start_server(server=server_handler)

    channel = transport.accept(1)
    if not channel is None:
        channel.close()

def main():
    print("HONEYPOT START")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SSH_PORT))
        server_socket.listen(100)

        paramiko.util.log_to_file ('/var/log/contrSSH/paramiko.log') 

        while(True):
            try:
                client_socket, client_addr = server_socket.accept()
		targets = open("/var/log/contrSSH/targets.txt", 'a')
		targets.write(client_addr[0] + '\n')
		targets.close()
		print(client_addr)
                thread.start_new_thread(handleConnection,(client_socket,))
            except Exception as e:
                print("ERROR: Client handling")
                print(e)

    except Exception as e:
        print("ERROR: Failed to create socket")
        print(e)
        sys.exit(1)

main()

