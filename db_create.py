#!/usr/bin/env python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO, LOG_FILE_NAME
from config import WORD_FILE
from app import db,models,app,user_datastore
from colorama import init
import logging
from logging.handlers import RotatingFileHandler
from hashlib import sha256
import os.path

init()
handler = RotatingFileHandler(LOG_FILE_NAME,maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

app.logger.info("About to call db.create_all().")
db.create_all()
app.logger.info("db.create_all() completed.")

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	app.logger.info("Creating database... {0}".format(SQLALCHEMY_DATABASE_URI))
	app.logger.info("Importing word lists...")
	c = 0
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
