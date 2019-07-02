import socket

LOCAL_SERV = PROD_SERV = TEST_SERV = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1063834827766-snp3s8f08gtb9rgeh9e13bsjqoq0bu8s.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'MuiPJXnlGqVfvia_G_0nUkzp'


SOCIAL_AUTH_FACEBOOK_KEY = '1372551116228229'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd90ee92f00eb53405daf25952ab06582'

# SOCIAL_AUTH_FACEBOOK_APP_KEY = '1372551116228229'
# SOCIAL_AUTH_FACEBOOK_APP_SECRET = 'd90ee92f00eb53405daf25952ab06582'

test_host = []
print("HOST", socket.gethostname())
deploy_host = ['green-liveconsole3', 'green-liveweb7']
if socket.gethostname() in deploy_host:
    print("TEST SERV")
    DEBUG = False
    PROD_SERV = True
    NAME_BASE = "bakz$bakz"
    USER_BASE = "bakz"
    PASSW_BASE = "Qwerty1234"
    HOST_BASE = 'bakz.mysql.pythonanywhere-services.com'
elif socket.gethostname() in test_host:
    print("TEST SERV")
    TEST_SERV = True
    DEBUG = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
else:
    print("LOCAL SERV")
    DEBUG = True
    LOCAL_SERV = True
    NAME_BASE = ""
    USER_BASE = ""
    PASSW_BASE = ""
