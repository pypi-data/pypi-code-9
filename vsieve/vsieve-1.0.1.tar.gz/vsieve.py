#!/usr/bin/env python3
#
# A "sieve of Eratosthenes" for integer vectors of length N.
#
# The original usage of this was for studying pythagorean triples and
# filtering out those that were simply multiples of smaller ones, e.g.
#
#    (5, 12, 13) as a "fundamental" Pythagorean triple vs
#   (10, 24, 26) as a multiple of (5, 12, 13)
#
# The code was then generalized to work for vectors of any length.
# Not sure entirely useful, but well here it is.
#
# Vector components MUST BE non-negative INTEGERS. 
#
# Mandating integers makes vector equivalency simple; it's either an
# integer multiple or it isn't; vs otherwise needing to define an
# epsilon tolerance for floating point values.
#
# Mandating positive just makes things simpler and avoids questions
# such as: is (8, -8, 8) a multiple of (-1, 1, -1) and if so, what
# other reflections/transformation should be allowed? Our answer: none.
#
# You will (or should) note that this is kind of a backwards sieve, in
# that the has() method is reporting composites (multiples of a seed)
# and also the seeds themselves; don't use has() if you are looking for
# the "primes" ... it's really the seeds() method that will report back
# to you the remaining primes (see the tests code at bottom for an
# example of this).
#
# IMPLEMENTATION:
#
# Within the sieve vectors are stored in a dictionary using their
# tuple as the key. If the vector is a seed the value stored is
# another vector indicating how far up this seed has been sieved. 
# If the vector is not a seed the value stored is irrelevant; it is
# merely the key presence that matters.
#
# Seeds are also recorded separately in __seeds so we can easily
# extend the sieve as necessary (without searching the entire sieve
# for the sieve vs. synthesized entries)
#
# The sieving is "somewhat" lazy. When you enter a seed we automatically
# sieve everything up to the point matching the magnitude of this new
# seed. After that we only sieve on demand based on magnitudes in the
# queries (the has() calls).
#

class VectorSieve:

    # Create a sieve of dimension n.
    # If you don't specify n it comes from the first vector you supply

    def __init__(self, n=None):
        self.__seeds = []      # the things you seeded (sort of; see _reseed)
        self.__sieve = {}      # the seeds plus their sieved multiples
        self.__sievemxg = 0    # max magnitude sieved
        self.__seeds_in_order = True
        self.dimension = n

    # Returns a copy of v as a tuple if v obeys all rules
    # Raises ValueError if any rules not obeyed
    #
    # Rules enforced are:
    #   * Vector dimensionality must match sieve dimensionality
    #   * All components must be non-negative integers
    #
    def check(self, v):

        n = len(v)
        if n != self.dimension:
            if self.dimension is None:  # you didn't spec at init time
                self.dimension = n      # so just take this as gospel
            else:
                raise ValueError("dim(v)={} != {}".format(n, self.dimension))

        # I suppose we could be more lenient here and accept int(c) == c
        # which would permit things like 4.0 ... but it just seems like
        # asking for trouble. For now integers enforced. I don't want to
        # get into having to implement "epsilon" checking for floating ops.
        for c in v:
            if (not isinstance(c, int)) or (c < 0):
                raise ValueError("vector components not non-negative integers")

        return tuple(v)


    # Add vector v into the sieve and (implicitly) sieve it.
    #
    def seed(self, v):
        v = self.check(v)   # throws ValueError if v illegal
        vmg2 = VectorSieve._mg2(v)

        # do nothing if we already have this one
        if self.__has(v, vmg2):
            return

        # ok, it's a seed...
        self.__seeds.append(v)        # remember it for resieving
        self.__sieve[v] = v           # initial max multiple

        # see if you've added out of magnitude order...
        if self.__seeds_in_order and len(self.__seeds) > 1:
            if vmg2 < VectorSieve._mg2(self.__seeds[-2]):
                self.__seeds_in_order = False

        # if this one is bigger than all previous...
        if vmg2 > self.__sievemxg:
            # everyone must be sieved up to here
            self._resieve_all(vmg2)
        else:
            # just bring this guy up to snuff
            self._resieve_this_vector(v, self.__sievemxg)

    #
    # Internal method used to extend sieving. Go through all the seeds
    # and add more of their multiples until they are all sieved past
    # the magnitude you are asking about
    #
    def _resieve_all(self, tarmg2):
        for v in self.__seeds:
            self._resieve_this_vector(v, tarmg2)
        self.__sievemxg = tarmg2   # this is now the new largest


    # Internal method: resieve one vector. Start where we left off
    # and keep adding more multiples to the sieve until we get past
    # the supplied target magnitude
    #
    def _resieve_this_vector(self, v, tarmg2):
        vx = self.__sieve[v]     # where it left off before

        while VectorSieve._mg2(vx) < tarmg2:
            # python2/python3 is why we need tuple() here...
            vx = tuple(map(lambda i,j: i+j, vx, v))
            self.__sieve[vx] = True   # add this to the sieve
        self.__sieve[v] = vx          # update current highest


    # Is the given vector in the sieve?
    # Returns v if so else None.
    #
    def has(self, v):
        return self.__has(self.check(v), VectorSieve._mg2(v))


    # internal version that bypasses input checks and avoids
    # having to recompute the squared-magnitude 
    #
    def __has(self, v, vmg2):

        # if you are asking beyond the point of where we've sieved so far...
        if vmg2 > self.__sievemxg:
            # go to double current max or just to here (if here is more)
            self._resieve_all(max(vmg2, 2*self.__sievemxg))

        try:
            # it is the mere success of this lookup that implies we have it
            x = self.__sieve[v]
            return v
        except KeyError:
            return None

    #
    # Return v if the given vector is a "seed" else None.
    #
    # To be a seed v must:
    #   - have been explicitly seeded via seed()
    #   - AND not be a multiple of another seed
    #
    # This automatically _reseeds() for you if necessary so for example:
    #
    #    v = VectorSieve(3)
    #    v.seed((6,8,10))
    #    s1 = v.is_seed((6,8,10))
    #    v.seed((3,4,5))
    #    s2 = v.is_seed((6,8,10))
    #
    # s1 will be (6,8,10) (i.e., not None) but s2 will be None because
    # after the insert of (3,4,5) the vector (6,8,10) is no longer a seed
    # (and: shame on you for adding seeds out of order)
    #
    def is_seed(self, v):
        v = self.check(v)

        self._reseed()          # method does nothing if not necessary
        return v if v in self.__seeds else None
 

    # 
    # Eliminate any "false" seeds that came about if you put seeds
    # into the sieve out of order. For example:
    #
    #    v = VectorSieve()
    #    v.seed((6,8,10))
    #    v.seed((3,4,5))
    #
    # In this case the second seed means the first vector (6,8,10) should
    # no longer be a seed. Really you aren't supposed to put vectors into
    # sieve "out of order" like that, but just for grins we correct if you do.
    #
    # You shouldn't normally call this yourself; it's done transparently.
    # And if you never put out-of-order seeds into the sieve then this
    # never happens.
    #
    def _reseed(self):
        if not self.__seeds_in_order:
            # you added them out of order, so sieve the seeds!
            seeds = sorted(self.__seeds, key=lambda v: VectorSieve._mg2(v)) 
            v = VectorSieve(self.dimension)
            for t in seeds:
                v.seed(t)
            v.__seeds_in_order = True   # bcs we just did it

            new_seeds = []

            for t in seeds:
                if v.is_seed(t):
                    new_seeds.append(t)

            self.__seeds = new_seeds
            self.__seeds_in_order = True


    # Return the seeds.
    # Returns a reseeded list (as a copy you can munge freely)

    def seeds(self):
        self._reseed()
        return self.__seeds.copy()


    # compute magnitude squared of a vector

    @staticmethod
    def _mg2(v):
        x = 0
        for c in v:
            x += c*c

        return x


#
# tests
#

if __name__ == "__main__":
    general_tests = [
        ( 'init'   , 4 ),
        ( 'seed'   , (1,1,1,1) ),
        ( 'has'    , (1,1,1,1) , (1,1,1,1) ),
        ( 'has'    , (2,2,2,2) , (2,2,2,2) ),
        ( 'has'    , (0,0,0,0) , None),
        ( 'has'    , (0,1,1,2) , None),
        ( 'seed'   , (9,9,9,9) ),
        ( 'is_seed', (1,1,1,1) , (1,1,1,1) ),
        ( 'is_seed', (2,2,2,2) , None),
        ( 'is_seed', (9,9,9,9) , None),
        ( 'init'   , 4 ),
        ( 'has'    , (2,2,2,2) , None ),
        ( 'has'    , (0,0,0,0) , None),
        ( 'seed'   , (9,9,9,9) ),
        ( 'has'    , (2,2,2,2) , None ),
        ( 'has'    , (0,0,0,0) , None),
        ( 'has'    , (90,90,90,90) , (90,90,90,90) ),
        ( 'has'    , (0,1,1,2) , None),
        ( 'seed'   , (1,1,1,1) ),
        ( 'has'    , (2,2,2,2) , (2,2,2,2) ),
        ( 'has'    , (9,9,9,9) , (9,9,9,9) ),
        ( 'is_seed', (9,9,9,9) , None),
        ( 'has'    , (1,1,1,1) , (1,1,1,1) ),
        ( 'is_seed', (1,1,1,1) , (1,1,1,1) ),
        ( 'is_seed', (2,2,2,2) , None),
        ( 'init'   , 3),
        ( 'seed'   , (60,80,100) ),
        ( 'has'    , (6,8,10), None),
        ( 'has'    , (600,800,1000), (600,800,1000) ),
        ( 'seed'   , (3,4,5)),
        ( 'has'    , (6,8,10), (6,8,10)),
        ( 'is_seed', (60, 80, 100), None),
        ( 'is_seed', (3,4,5), (3,4,5)),
        ( 'is_seed', (6,8,10), None),
        ( 'init'   , None),
        ( 'seed'   , (3,4,5)),
        ( 'has'    , (3,4,5), (3,4,5)),
        ( 'seed'   , (5,12,13)),
        ( 'has'    , (5,12,13), (5,12,13)),
        ( 'has'    , (50,120,130), (50,120,130)),
        ( 'has'    , (30,40,50), (30,40,50)),
        ( 'init'   , None),
        ( 'seed'   , (5,12,13)),
        ( 'seed'   , (3,4,5)),
        ( 'has'    , (5,12,13), (5,12,13)),
        ( 'has'    , (50,120,130), (50,120,130)),
        ( 'has'    , (30,40,50), (30,40,50)),
        ( 'is_seed', (6,8,10), None),
        ( 'init'   , 5),
        ( 'seed'   , (0,0,1,0,0)),
        ( 'has'    , (0,0,0,100,0), None),
        ( 'has'    , (0,0,100,0,0), (0,0,100,0,0)),
        ( 'init'   , 3),
        ( 'seed'   , (6,8,10)),
        ( 'is_seed', (6,8,10), (6,8,10)),
        ( 'seed'   , (3,4,5)),
        ( 'is_seed', (6,8,10), None)
    ]


    v = None
    for t in general_tests:
        if t[0] == 'init':
            v = VectorSieve(t[1])
        elif t[0] == 'seed':
            v.seed(t[1])
        elif t[0] == 'has':
            if v.has(t[1]) != t[2]:
                print("FAIL: ", t)
                exit(1)
        elif t[0] == 'is_seed':
            if v.is_seed(t[1]) != t[2]:
                print("FAIL: ", t)
                exit(1)
        else:
            print("WTF", t)
            exit(1)

    #
    # Make a 1-dimensional sieve and actually do the sieve of E algorithm
    # Check results against this table of primes that was generated with a
    # different program (so as to actually have some verification attributes)

    primes = ( 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
       53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
       127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
       193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263,
       269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
       349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421,
       431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
       503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593,
       599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661,
       673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757,
       761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853,
       857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
       947, 953, 967, 971, 977, 983, 991, 997 )

    primelimit = 1000

    v = VectorSieve(1)
    for i in range(2, primelimit):
        v.seed((i,))             # force tuple vs just an int in parens

    # at this point the true seeds should be the primes
    seeds = v.seeds()

    if len(primes) != len(seeds):
        print("Wrong number of primes")
        exit(1)

    for p in primes:
        if (p,) not in seeds:
            print("Missing prime ", p)
            exit(1)

    # now try it again with dimensions varying N just for yucks, as follows:
    for dm in range(2,10):
        v = VectorSieve(dm)
        z = [0] * dm
        for i in range(2, primelimit):
            z[-2] = i
            v.seed(z)

        seeds = v.seeds()
        if len(primes) != len(seeds):
            print("Wrong number of primes for dimension ",dm)
            exit(1)

        for p in primes:
            z[-2] = p
            if tuple(z) not in seeds:
                print("Missing prime ", p, "at dim", dm)
                exit(1)


    # this variation puts multiple primes per tuple
    for dm in range(6,20):
        v = VectorSieve(dm)
        z = [0] * dm
        for i in range(2, primelimit):
            z[-2] = i
            z[-3] = i
            z[-5] = i
            z[0] = i
            v.seed(z)

        seeds = v.seeds()
        if len(primes) != len(seeds):
            print("Wrong number of primes for dimension ",dm)
            exit(1)

        for p in primes:
            z[-2] = p
            z[-3] = p
            z[-5] = p
            z[0] = p
            if tuple(z) not in seeds:
                print("Missing prime ", p, "at dim", dm)
                exit(1)

    print("All Tests Passed!")
