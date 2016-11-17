import hashlib

def getsha256(s):
    return hashlib.sha256(s).hexdigest()