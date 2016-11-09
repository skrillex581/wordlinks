from itertools import chain, combinations, permutations

from flask import jsonify, make_response
from sqlalchemy.sql.expression import func

from app import app, db
from app.utils.spgraph import PathNotFound
from models import Word
from wordlist import Graph


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


@app.route('/wordsapi/v1.0/words/anagram/<string:word1>/',methods=['GET'])
def get_anagram(word1):    
    return jsonify(result=getanagrams(word1,4))

def getanagrams(word1,minwordlength=0):
    result = []
    b = []    
    letters = list(sorted(word1))        
    for z in chain.from_iterable(combinations(letters, r) for r in range(len(letters)+1)):        
        result.append(''.join(z))
    print result
    for j in result:
        words = Word.query.filter_by(sortedword=j).all()
        for w in words:
            print w.word
            if len(w.word) >= minwordlength:
                b.append(w.word)
    return sorted(list(set(b)))

@app.route('/wordsapi/v1.0/words/updatedsortedfield',methods=['GET'])
def updatesorted():
    for w in Word.query.all():
        w.sortedword = ''.join(sorted(w.word))
        db.session.add(w)
    db.session.commit()
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
