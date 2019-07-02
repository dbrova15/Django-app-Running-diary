import socket

debug_host = ['MI-Bakz']
if socket.gethostname() in debug_host:
    DEBUG = False
else:
    DEBUG = True
