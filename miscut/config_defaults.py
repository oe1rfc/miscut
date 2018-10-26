DEBUG = True

SECRET_KEY = '123456790'

SECURITY_PASSWORD_SALT = "changeme"
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"
SECURITY_RESET_URL = "/lostpass/"

#API_TOKEN = "foobar"

SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_EMAIL_SENDER = "root@localhost"

SECURITY_POST_LOGIN_VIEW = "/"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_POST_REGISTER_VIEW = "/"

MAIL_SUPPRESS_SEND = True
MAIL_DEFAULT_SENDER = "WebCut <root@localhost>"
MAIL_SERVER = "localhost"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/sample_db.sqlite'
