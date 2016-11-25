import os
from getpass import getpass
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG=True
WTF_CSRF_ENABLED = True
SECRET_KEY = "26-J0um@S3p035-p13LK0P"
SQLALCHEMY_DATABASE_URI = "mysql://words:wordsdev@192.168.0.21/wordlist"  #'sqlite:///' + os.path.join(basedir, 'wordlit.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_FILE_NAME = "app.log"
# administrator list
ADMINS = ["mailbox@a20.co.za"]
WORD_FILE = "enwords.txt"
WORD_FILE_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words2.txt"
# mail server settings
# python -m smtpd -n -c DebuggingServer localhost:25
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_DEFAULT_SENDER = "No-reply <{0}>".format(ADMINS[0])
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_DEBUG = True
MAIL_USERNAME = "alphacat01@gmail.com"
MAIL_SUPPRESS_SEND = False
if not "CAT_CART" in os.environ:
    MAIL_PASSWORD = getpass("Enter the password to mail account '{0}': ".format(MAIL_USERNAME))    
    os.environ["CAT_CART"] = str(MAIL_PASSWORD)
MAIL_PASSWORD = os.environ["CAT_CART"]


#flask-security
SECURITY_PASSWORD_HASH = "sha512_crypt"
SECURITY_PASSWORD_SALT = "greencAmpIr546}.#2}?" #really unconnected salt
SECURITY_EMAIL_SENDER = "meego <{0}>".format(ADMINS[0])
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = False

