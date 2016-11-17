from app import db
from hashlib import md5
from app import app
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required 



import sys

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
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
