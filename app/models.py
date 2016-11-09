from app import db
from hashlib import md5
from app import app

import sys

class Word(db.Model):
	__tablename__ = 'words'
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(30), index=True, unique=True)
	wordlength = db.Column(db.Integer, index=True)
	sortedword = db.Column(db.String(30),index=True)
	@property
	def serialize(self):
		"""serialize this baby"""
		return {
			'w':self.word			
		}
	def __repr__(self):
		return '%s'%(self.word)
