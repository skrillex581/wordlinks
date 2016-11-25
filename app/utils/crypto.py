import hashlib

def getsha256(s):
    return hashlib.sha256(s).hexdigest()
def getsha512(s):
    return hashlib.sha512(s).hexdigest()