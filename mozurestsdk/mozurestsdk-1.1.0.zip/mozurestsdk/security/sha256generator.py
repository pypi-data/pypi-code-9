import hashlib;

class sha256generator(object):
	"""Generate a sha1 value to validate mozu events or form posts"""

	def getHash(sharedSecret, date, body):
		hashString = sharedSecret+sharedSecret;
		m = hashlib.sha256(hashString.encode());
		m.digest();
		hash1 = m.hexdigest();

		hashString = hash1+date+body;
		m = hashlib.sha256(hashString.encode());
		m.digest();
		return m.dexdigest();
		