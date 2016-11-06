import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://words:wordsdev@192.168.0.21/wordlist'  #'sqlite:///' + os.path.join(basedir, 'wordlit.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WORD_FILE = 'enwords.txt'
# mail server settings
# python -m smtpd -n -c DebuggingServer localhost:25
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']
