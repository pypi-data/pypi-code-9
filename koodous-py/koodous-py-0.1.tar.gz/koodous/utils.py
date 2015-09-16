import hashlib


def sha256(tfile):
    f = open(tfile, 'rb')
    hasher_256 = hashlib.sha256()
    fr = f.read(1024)   
    while(fr):
        hasher_256.update(fr)
        fr = f.read(1024)

    return hasher_256.hexdigest()