"""Module for the backend of deterministicpwgen. Handles things such as
the generation of passwords and the creation/loading of keyfiles.
"""

import hashlib
import os

class SeededRandom(object):
	"""A seeded random object. Given the same seed, it should recreate
	the same stream of bytes every time.
	"""

	# This seed is always prepended to the hash candidate.  
	STATIC_SEED = "\x17>\xef\x92\xd7\xc9i!\xd3\x8a_\x80W" \
                  "\xcd\x94\xeen\xa6\xac|\xaa\xea\xdeO\x0c\xf8H!G\xcal\xa5"
	
	def __init__(self, seed):
		self.data = ""
		self.enabled = True
		self.nonce = 0
		self.seed = seed
	
	def random_bytes(self, n):
		"""Returns n bytes worth of random data."""
		
		if not self.enabled:
			raise ValueError("This SeededRandom object is closed.")
		elif n < 0:
			raise ValueError("Impossible; cannot return bytes where n < 0.")
		elif not isinstance(n, (long, int)):
			raise ValueError("n must be an numeric value.")
			
		requested = ""
		while len(self.data) < n:
			candidate = SeededRandom.STATIC_SEED + self.seed + str(self.nonce)
			self.data += hashlib.sha512(candidate).digest()
			self.nonce += 1

		requested, self.data = self.data[:n], self.data[n:]
		
		# Throw an AssertionError if too little bytes; should never occur.  
		assert len(requested) == n
		return requested
	
	def close(self):
		"""Close the RNG."""
		self.enabled = False

DIRECTORY = os.path.expanduser("~") + os.sep + ".deterministicpwgen" + os.sep

def directory_exists():
    return os.path.isdir(DIRECTORY)

def create_directory():
    if not directory_exists():
        os.mkdir(DIRECTORY)

def keyfile_exists(name="keyfile"):
    """Checks if the keyfile exists."""
    global DIRECTORY
    return os.path.isfile(DIRECTORY + name)

def create_keyfile(name="keyfile", size=4096, permissions=0600):
    """Creates a keyfile to the specification provided in the arguments."""
    global DIRECTORY
    
    path = DIRECTORY + name
    create_directory()

    if os.path.isfile(path):
        raise IOError("Keyfile already exists under %s!" % path)
    
    f = open(path, "w")

    # Write n bytes of random data from /dev/urandom.  
    f.write(os.urandom(size))
    f.close()
    os.chmod(path, permissions)

def load_keyfile_seed(name="keyfile"):
    """Returns the seed found in the keyfile."""
    global DIRECTORY

    path = DIRECTORY + name
    try:
        f = open(path, "r")
        seed = f.read()
        return seed
    except IOError:
        raise IOError("Keyfile doesn't exist at %s." % path)

def stretch_key(key, rounds=65536, salt=""):
	"""Streches a key by a default of 65536 rounds. This is particularly
	important for security.
	"""
	stretched = key
	for i in range(rounds):
		stretched = hashlib.sha512(stretched + key + salt).digest()
	return stretched

def generate(seed, length, charset):
    """Returns a random string to the specification of the arguments."""
    sr = SeededRandom(seed)
    by = sr.random_bytes(length)
    sr.close()

    return "".join(charset[ord(i) % len(charset)] for i in by)
