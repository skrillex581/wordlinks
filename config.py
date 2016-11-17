import os
from getpass import getpass
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG=True
WTF_CSRF_ENABLED = True
SECRET_KEY = "m48Xyp70wZTzVEjfLeHv pint of stale milk"
SQLALCHEMY_DATABASE_URI = "mysql://words:wordsdev@192.168.0.21/wordlist"  #'sqlite:///' + os.path.join(basedir, 'wordlit.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_FILE_NAME = "app.log"

WORD_FILE = "enwords.txt"
# mail server settings
# python -m smtpd -n -c DebuggingServer localhost:25
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = "No-reply <mailbox@a20.co.za>"
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_DEBUG = True
MAIL_USERNAME = "alphacat01@gmail.com"
MAIL_SUPPRESS_SEND = False
if not "MAIL_PASSWORD" in os.environ:
    MAIL_PASSWORD = getpass("Enter the password to mail account '{0}': ".format(MAIL_USERNAME))
    os.environ["MAIL_PASSWORD"] = MAIL_PASSWORD
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
print os.environ["MAIL_PASSWORD"]
# administrator list
ADMINS = ["mailbox@a20.co.za"]



#flask-security
SECURITY_PASSWORD_HASH = "sha512_crypt"
SECURITY_PASSWORD_SALT = "greencAmpIr546}.#2}?"
SECURITY_EMAIL_SENDER = "meego <mailbox@a20.co.za>"
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = False

