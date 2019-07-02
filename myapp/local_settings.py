import socket

# debug_host = ['local_host', '127.0.0.1']
ALLOWED_HOSTS = ["bakz.pythonanywhere.com"]
if socket.gethostname() not in ALLOWED_HOSTS:
    DEBUG = False
else:
    DEBUG = True
