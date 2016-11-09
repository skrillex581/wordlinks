from app.models import Word
from app import db

for w in Word.query.all():
	w.sortedword = ''.join(sorted(w.word))	
	db.session.add(w)
db.session.commit()
