from app import app,db
from flask import jsonify
from models import Word

from sqlalchemy.sql.expression import func

@app.route('/')
@app.route('/index')
def index():
	return "Hello world."


@app.route('/wordsapi/v1.0/words/<int:length>',methods=['GET'])
def get_wordsbylength(length):
	words = Word.query.filter_by(wordlength=length)
	result = [w.serialize for w in words.all()]	
	return jsonify(json_list=result)

@app.route('/wordsapi/v1.0/words/<int:length>/count',methods=['GET'])
def get_wordsbylengthcount(length):
	wordcount = Word.query.filter_by(wordlength=length).count()
	return jsonify(count=wordcount)
