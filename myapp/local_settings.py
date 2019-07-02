import socket


deploy_host = ['green-liveconsole3']
if socket.gethostname() in deploy_host:
    DEBUG = False
else:
    DEBUG = True
