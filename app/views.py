from itertools import chain, combinations, permutations
import logging
from forms import RegistrationForm
from flask import jsonify, make_response, render_template,request
from flask_mail import Message
from flask_user import login_required, UserManager, UserMixin
from sqlalchemy.sql.expression import func

from app import app, db, mail
from app.utils.spgraph import PathNotFound
from models import Word
from wordlist import Graph


# tears->smile
@app.route('/')
@app.route('/index')
def index():
    msg = Message("Hello",recipients=["mailbox@a20.co.za"])
    mail.send(msg)
    return render_template('index.html',user={})
@app.route('/logoutuser')
def logoutuser():
    return render_template('index.html')
@app.route('/closemyaccount')
def closemyaccount():
    return render_template('closemyaccount.html')
@app.route('/approvals')
def approvals():
    return render_template('approvals.html')

@app.route('/register', methods=['GET','POST'])
def register():    
    form = RegistrationForm(txEmail="zahirj@mweb.co.za")
    if request.method=="GET":
        app.logger.info("This is a get")
    else:
        app.logger.info("This is a POST")    
    return render_template("register.html", user={}, form=form)
@app.route('/about')
def about():
    return render_template('about.html')    
@app.route('/login')
def login():
    return render_template('login.html')


# API 

@app.route('/wordsapi/v1.0/words/<int:length>',methods=['GET'])
def get_wordsbylength(length):
    words = Word.query.filter_by(wordlength=length)
    result = [w.serialize for w in words.all()]	
    return jsonify(words=result,error='')

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
