'''This file defines constants used by romgw, gwsurrogate and gwtools'''

'''import sys
if hasattr(sys, '_called_from_test'):
  print "Called from within a test run"
  # older constants (outdated 7/9/2015) -- keep for regression testing
  c         = 2.99792458e8     # Speed of light (MKS)
  G         = 6.67428e-11      # Gravitation constant (MKS)
  Msun      = 1.98892e30       # Solar mass (kg)
  Msuninsec = Msun * G / c**3  # Solar mass (secs)
  Mpcinm    = 3.08568025e22    # Megaparsecs (m)
  Mpcinkm   = Mpcinm/1000.0    # Megaparsecs (km)

else:
  print "Using LAL values for constants"
  # These contants are found in LAL code
  c         = 299792458.0
  G         = 6.67384e-11
  Msun      = 1.9885469549614615e+30
  Msuninsec = Msun * G / c**3 # TODO: check the product obtains ~11 digits of accuracy
  Mpcinm    = 3.085677581491367e+22
  Mpcinkm   = Mpcinm/1000.0    # Megaparsecs (km)
  Msuninkg = Msun'''

# romgw constants, and older gwsurroate constants # 
# TODO: consider keeping these in favor of lal constants
# commented out above. The codes will reproduce previous results.
c         = 2.99792458e8     # Speed of light (MKS)
G         = 6.67428e-11      # Gravitation constant (MKS)
Msun      = 1.98892e30       # Solar mass (kg)

# TODO: Msuninsec should be hardcoded -- its known to more digits than G or Msum
Msuninsec = Msun * G / c**3  # Solar mass (secs)

Mpcinm    = 3.08568025e22    # Megaparsecs (m)
Mpcinkm   = Mpcinm/1000.0    # Megaparsecs (km)
Msuninkg  = Msun             # for romgw 

"""Euler-Mascheroni constant"""
gamma_E = 0.577215664901532


# Jonathan's constants
#Msun = 1.9891e30
#Mpcinm = 3.08567758e22
#SPEED_OF_LIGHT_C = 299792458
#GRAVITATIONAL_CONSTANT_G = 6.67384e-11
#G = 6.67384e-11
#Msuninsec = Msun * G / c**3
#Mpcinkm   = Mpcinm/1000.0    # Megaparsecs (km)

