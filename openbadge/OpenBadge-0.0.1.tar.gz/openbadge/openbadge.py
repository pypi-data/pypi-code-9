import hashlib
import jwt
import time
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Keys():
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def assertion(self, email, badge_url):
        salt = id_generator()
        hashed_email = 'sha256$' + hashlib.sha256(email.lower() + salt).hexdigest()
        assertion = {"uid": id_generator(),
                     "recipient": {"identity": hashed_email, "type": "email", "hashed": True, "salt": salt},
                     "badge": badge_url,
                     "verify": {"url": self.public_key, "type": "signed"},
                     "issuedOn": int(time.time())}
        # Sign with private key
        encoded = jwt.encode(assertion, self.private_key, algorithm='RS256', headers={'alg': 'RS256'})
        return encoded.decode("utf-8")