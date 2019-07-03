import socket

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "super secret key"
ALLOWED_HOSTS = [""]

LOCAL_SERV = PROD_SERV = TEST_SERV = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

print("HOST", socket.gethostname())

test_hosts = ['']  # list of test servers
deploy_hosts = ['']  # list of production servers

if socket.gethostname() in deploy_hosts:
    print("TEST SERV")
    DEBUG = False
    PROD_SERV = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
    HOST_BASE = ""

elif socket.gethostname() in test_hosts:
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
