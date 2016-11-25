from itertools import chain, combinations, permutations
import logging
from forms import RegistrationForm
from flask import jsonify, make_response, render_template,request,g
from flask_mail import Message
from sqlalchemy.sql.expression import func

from app import app, db, mail
from app.utils.spgraph import PathNotFound
from app.utils.crypto import getsha512
from models import Word, User, Role
from wordlist import Graph, getscrabblescore

from flask_security import login_required, current_user
from flask_security.utils import encrypt_password
from utils.crypto import getsha256
import  config 
from app import user_datastore, security

 
# tears->smile

@app.route('/')
@app.route('/index')
def index():    
    
    return render_template('index.html',user={})

@app.route('/apihelper')
def showapihelper():    
    return render_template('api.html')

@app.route('/logoutuser')
def logoutuser():
    return render_template('index.html')

@app.route('/closemyaccount')
def closemyaccount():
    return render_template('closemyaccount.html')

@app.route('/approvals')
def approvals():
    return render_template('approvals.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')    

@app.route('/target')
@login_required
def target():
    return render_template('target.html')

@app.route('/wordladder')
@login_required
def wordladder():
    return render_template('target.html')

# API 

@app.route('/wordsapi/v1.0/words/<int:length>',methods=['GET'])
def get_wordsbylength(length):
    words = Word.query.filter_by(wordlength=length)
    result = [w.word for w in words.all()]	
    return jsonify(words=result,error='')
    
@app.route('/wordsapi/v1.0/words/getscrabblescore/<string:word>',methods=['GET'])
def get_scrabbblescrore(word):
    return jsonify(score=getscrabblescore(word))

@app.route('/wordsapi/v1.0/words/<int:length>/count',methods=['GET'])
def get_wordsbylengthcount(length):
    wordcount = Word.query.filter_by(wordlength=length).count()
    return jsonify(count=wordcount)


@app.route('/wordsapi/v1.0/words/anagram/<string:word1>/',defaults={'letter':None,'minwordlength':4},methods=['GET'])
@app.route('/wordsapi/v1.0/words/anagram/<string:word1>/<int:minwordlength>/<string:letter>/',methods=['GET'])
def get_anagram(word1,minwordlength,letter):    
    words = getanagrams(word1,minwordlength,letter)
    stats = {}
    stats["wordcount"] = len(words)
    stats["shortestwordlength"] = len(sorted(words,key=lambda w:len(w))[:-1][0])
    stats["longestwordlength"] = len(sorted(words,key=lambda w:len(w))[-1:][0])
    stats["longestwords"] = filter(lambda w:len(w)==stats["longestwordlength"],words)

    return jsonify(words=words,stats=stats,error='')

def getanagrams(word1,minwordlength=0,letter=None):    
    result = []
    b = []
    t = '' 
    letters = list(sorted(word1))        
    for z in chain.from_iterable(combinations(letters, r) for r in range(len(letters)+1)):        
        t = ''.join(z)
        if len(t) >= minwordlength and (letter in t if letter else True):
            result.append(''.join(t))
    for j in result:
        words = Word.query.filter_by(sortedword=j).all()
        for w in words:                        
            b.append(w.word)
    return sorted(list(set(b)))

@app.route('/wordsapi/v1.0/words/updatesortedfield',methods=['GET'])
def updatesorted():
    for w in Word.query.all():
        w.sortedword = ''.join(sorted(w.word))
        db.session.add(w)
    db.session.commit()


@app.route('/wordsapi/v1.0/words/ladder/<string:word1>/<string:word2>/',methods=['GET'])
def get_wordladder(word1, word2):
    app.logger.info("Trying to find ladder between {0} and {1}".format(word1,word2))
    if not len(word1.strip())==len(word2.strip()):
        return make_response(jsonify(error='Word lengths do not match.'),500)
    else:
        g = Graph("/home/marmite/kratosdb")	
        g.BuildMatchingsFromDatabase(len(word1))
        try:
            return jsonify(error='',words=g.FindLadder(word1,word2))
        except PathNotFound,e:	
            return make_response(jsonify(words=[],error='Path not found between %s and %s'%(word1,word2)),500)


#####################
@app.before_first_request
def create_initial_data():
    msg = Message("Application has started.",recipients=config.ADMINS)        
    mail.send(msg)    
    pass

@app.before_request
def before_request():
    print "Request has been made."
    g.user = current_user