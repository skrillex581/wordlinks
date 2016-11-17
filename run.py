#!/usr/bin/env python

from app import app
import logging
import sys
from logging.handlers import RotatingFileHandler 
from config import LOG_FILE_NAME

handler = RotatingFileHandler(LOG_FILE_NAME,maxBytes=1024000,backupCount=2)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
app.logger.addHandler(ch)

app.run(debug=True)
app.logger.info('Application started...')
