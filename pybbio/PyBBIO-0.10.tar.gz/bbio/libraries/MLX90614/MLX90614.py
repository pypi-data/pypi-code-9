"""

"""

class MLX90614(object):
  I2C_ADDR = 0x5a

  CRC_DIVISOR = 0b100000111

  def __init__(self, i2c_bus):
    self.i2c_bus = i2c_bus

  def readObjectTempC(self):
    lsb, msb, pec = self.i2c_bus.readTransaction(self.I2C_ADDR, 0x07, 3)
    raw_value = (msb<<8) | lsb
    #assert self.checkCRC(raw_value, pec), "received invalid data"
    self.checkCRC(raw_value, pec)
    tempk = raw_value*0.02 # temp in Kelvin
    return tempk - 273.75 # Convert to Celsius

  def readAmbientTempC(self):
    lsb, msb, pec = self.i2c_bus.readTransaction(self.I2C_ADDR, 0x06, 3)
    raw_value = (msb<<8) | lsb
    #assert self.checkCRC(raw_value, pec), "received invalid data"
    self.checkCRC(raw_value, pec)
    tempk = raw_value*0.02 # temp in Kelvin
    return tempk - 273.75

  def checkCRC(self, value, crc):
    """ Checks the given 2-byte value against the given CRC
        
    Uses the MLX90614's divisor polynomial of x^8 + x^2 + x^1 + 1 given in 
    the datasheet.
    See http://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks
    """
    value <<= 8
    divisor = self.CRC_DIVISOR << 15
    for i in range(16):
      if value & 1<<(23-i):
        # There's a 1 above the x^8 bit of the divisor polynomial
        value ^= divisor
      divisor >>= 1
    if (value & 0xff) == crc: return True
    return False
