import socket

LOCAL_SERV = PROD_SERV = TEST_SERV = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

test_host = []
print("HOST", socket.gethostname())
deploy_host = ['', '']
if socket.gethostname() in deploy_host:
    print("TEST SERV")
    DEBUG = False
    PROD_SERV = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
    HOST_BASE = ""
elif socket.gethostname() in test_host:
    print("TEST SERV")
    DEBUG = True
    TEST_SERV = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
    HOST_BASE = ""
else:
    print("LOCAL SERV")
    DEBUG = True
    LOCAL_SERV = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
    HOST_BASE = ""
