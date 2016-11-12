import os
from getpass import getpass
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = "m48Xyp70wZTzVEjfLeHv"
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
MAIL_PASSWORD = ""
if not "MAIL_PASSWORD" in os.environ:
    MAIL_PASSWORD = getpass("Enter the password to mail account '{0}': ".format(MAIL_USERNAME))
    os.environ["MAIL_PASSWORD"] = MAIL_PASSWORD
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]
print MAIL_USERNAME
print MAIL_PASSWORD
print os.environ["MAIL_PASSWORD"]
# administrator list
ADMINS = ["mailbox@a20.co.za"]
