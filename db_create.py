#!/usr/bin/env python 

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO, LOG_FILE_NAME
from config import WORD_FILE,WORD_FILE_URL

from app import db,models,app, user_datastore
from app.utils.toolbox import FileDownloader
from flask_security.utils import encrypt_password
from colorama import init
import logging
from logging.handlers import RotatingFileHandler
import os.path

init()
handler = RotatingFileHandler(LOG_FILE_NAME,maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.info("About to call db.create_all().")
db.create_all()
#create a default user
user_datastore.create_user(email='buttsmckraken@bikinibottom.com', password=encrypt_password('password'))
db.session.commit()
app.logger.info("db.create_all() completed.")
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	app.logger.info("Creating database... {0}".format(SQLALCHEMY_DATABASE_URI))
	app.logger.info("Importing word lists...")
	app.logger.info("Downloading wordlist from {0}".format(WORD_FILE_URL))
	c = 0
	d = FileDownloader(WORD_FILE_URL)
	d.DownloadUrl(WORD_FILE)
	app.logger.info("Wordlist downloaded and saved to {0}".format(WORD_FILE))
	if os.path.isfile(WORD_FILE):
		with open(WORD_FILE) as f:
			for line in f:
				c += 1
				line = line.strip()
				w = models.Word(word=line, wordlength=len(line), sortedword=''.join(sorted(line)))
				db.session.add(w)
		db.session.commit()
		app.logger.info("Completed.")
		app.logger.info("%d words added." %(c))
	else:
		app.logger.info("World file not found '{0}'. Could not create word list.".format(WORD_FILE))
	
else:
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
