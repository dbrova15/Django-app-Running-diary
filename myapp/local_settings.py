import socket

LOCAL_SERV = PROD_SERV = TEST_SERV = False

test_host = []
deploy_host = ['green-liveconsole3']
if socket.gethostname() in deploy_host:
    PROD = True
    PROD_SERV = True
elif socket.gethostname() in test_host:
    TEST_SERV = True
    DEBUG = True
else:
    DEBUG = True
    LOCAL_SERV = True
