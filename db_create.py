#!/usr/bin/env python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from config import WORD_FILE
from app import db,models
from colorama import init

import os.path

print SQLALCHEMY_MIGRATE_REPO
print SQLALCHEMY_DATABASE_URI
print WORD_FILE

init()
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print "Importing word lists..."
	c = 0
	if os.path.isfile(WORD_FILE):		
		with open(WORD_FILE) as f:
			for line in f:
				c +=1
				line = line.strip()
				w= models.Word(word=line,wordlength=len(line))
				db.session.add(w)
		db.session.commit()		
		print "%d words added." %(c)
	else:
		print Fore.RED + "World file not found. Could not create word list."
		print Style.RESET_ALL 
	
else:
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
