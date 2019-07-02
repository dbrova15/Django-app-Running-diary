import socket

debug_host = ['local_host', '127.0.0.1']

if socket.gethostname() in debug_host:
    DEBUG = False
else:
    DEBUG = True
