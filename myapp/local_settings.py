import socket

LOCAL_SERV = PROD_SERV = TEST_SERV = False

test_host = []
print("HOST", socket.gethostname())
deploy_host = ['green-liveconsole3', 'green-liveweb7']
if socket.gethostname() in deploy_host:
    DEBUG = False
    PROD_SERV = True
elif socket.gethostname() in test_host:
    TEST_SERV = True
    DEBUG = True
else:
    DEBUG = True
    LOCAL_SERV = True
