from app import app,db
from flask import jsonify,make_response
from models import Word
from wordlist import Graph
from app.utils.spgraph import PathNotFound
from sqlalchemy.sql.expression import func
# tears->smile
@app.route('/')
@app.route('/index')
def index():
	return "Hello world."


@app.route('/wordsapi/v1.0/words/<int:length>',methods=['GET'])
def get_wordsbylength(length):
	words = Word.query.filter_by(wordlength=length)
	result = [w.serialize for w in words.all()]	
	return jsonify(result=result)

@app.route('/wordsapi/v1.0/words/<int:length>/count',methods=['GET'])
def get_wordsbylengthcount(length):
	wordcount = Word.query.filter_by(wordlength=length).count()
	return jsonify(result=wordcount)

@app.route('/wordsapi/v1.0/words/ladder/<string:word1>/<string:word2>/',methods=['GET'])
def get_wordladder(word1, word2):
    if not len(word1.strip())==len(word2.strip()):
        return make_response(jsonify(Error='Word lengths do not match.'),500)
    else:
		g = Graph("/home/marmite/kratosdb")	
		g.BuildMatchingsFromDatabase(len(word1))
		try:
			return jsonify(result=g.FindLadder(word1,word2))
		except PathNotFound,e:	
			return make_response(jsonify(Error='Path not found between %s and %s'%(word1,word2)))
