"""
 MAX7219
 Copyright 2015 - Alexander Hiam <alex@graycat.io>

 A PyBBIO library for controlling MAX7219 8-digit LED display driver.

 MAX7219 is released as part of PyBBIO under its MIT license.
 See PyBBIO/LICENSE.txt
"""


class MAX7219(object):
  REG_DECODE_MODE  = 0x9
  REG_INTENSITY    = 0xa
  REG_SCAN_LIMIT   = 0xb
  REG_SHUTDOWN     = 0xc
  REG_DISPLAY_TEST = 0xf

  def __init__(self, spi_bus, spi_cs):
    self.spi_bus = spi_bus
    self.spi_cs = spi_cs

    self.writeRegister(self.REG_INTENSITY, 0)

  def clear(self):
    """ Writes 0 to all digit registers. 
    """
    for digit in range(1, 9):
      self.writeRegister(digit, 0)

  def fill(self):
    """ Writes 0xff to all digit registers. 
    """
    for digit in range(1, 9):
      self.writeRegister(digit, 0xff)

  def writeDigit(self, digit, value):
    """ Writes the given 8-bit value to the given digit in the range 0-7.
    """
    if not (0 <= digit <= 7):
      raise ValueError("digit mosut be in range 0-7")
    digit += 1
    self.writeRegister(digit, value)

  def setIntensity(self, intensity):
    """ Sets the display intensity by changing the duty cycle at which each 
        LED is driven. The allowed range is 0-15.
    """
    if type(intensity) != int:
      raise TypeError("'intensity' must be an int") 
    if not (0 <= intensity <= 15):
      raise ValueError("'addr' must be in range 0-15")     
    self.writeRegister(self.REG_INTENSITY, intensity)

  def enableDisplayTest(self):
    self.writeRegister(self.REG_DISPLAY_TEST, 0x1)

  def disableDisplayTest(self):
    self.writeRegister(self.REG_DISPLAY_TEST, 0x0)

  def writeRegister(self, addr, value):
    """ Writes the given value to the given register address. 
    """
    if type(addr) != int:
      raise TypeError("'addr' must be an int") 
    if not (0 <= addr <= 15):
      raise ValueError("'addr' must be in range 0-255") 

    if type(value) != int:
      raise TypeError("'value' must be an int") 
    if not (0 <= value <= 255):
      raise ValueError("'value' must be in range 0-255") 

    data = (addr<<8) | value

    self.setSPIConfig()
    self.spi_bus.write(self.spi_cs, [data])

  def setSPIConfig(self):
    """ Configures the SPI bus per MAX7219 settings. 
    """
    self.spi_bus.setClockMode(self.spi_cs, 0)
    self.spi_bus.setMaxFrequency(self.spi_cs, 10000000)
    self.spi_bus.setBitsPerWord(self.spi_cs, 16)
    self.spi_bus.setMSBFirst(self.spi_cs)



class LEDMatrix(MAX7219):
  def __init__(self, spi_bus, spi_cs):
    self._buffer = [0]*8*8

    super(LEDMatrix, self).__init__(spi_bus, spi_cs)
    self.writeRegister(self.REG_SHUTDOWN, 0)
    self.disableDisplayTest()
    self.writeRegister(self.REG_DECODE_MODE, 0)
    self.writeRegister(self.REG_SCAN_LIMIT, 7)
    self.writeRegister(self.REG_SHUTDOWN, 1)

    self.clear()

  def clearBuffer(self):
    """
    """
    for i in range(len(self._buffer)):
      self._buffer[i] = 0

  def clear(self):
    """
    """
    self.clearBuffer()
    self.update()

  def setBuffer(self, buf):
    """
    """
    if len(buf) != 64:
      raise ValueError("buf must be length 64 (8x8)") 
    self._buffer = buf[::]

  def writeBuffer(self, buf):
    """
    """
    self.setBuffer(buf)
    self.update()
    
  def setPixel(self, x, y, state):
    """
    """
    self._buffer[y*8 + x] = 1 if state else 0

  def writePixel(self, x, y, state):
    """
    """
    self.setPixel(x, y, state)
    column = y
    state = self._getColumn(column, self._buffer)
    self.writeColumn(column, state)

  def update(self):
    """
    """
    for column in range(8):
      self.writeColumn(column, self._getColumn(column, self._buffer))

  def writeColumn(self, column, value):
    """
    """
    self.writeDigit(column, value)

  def _getColumn(self, column, buf):
    """
    """
    value = 0
    for i in range(8):
      if buf[column*8 + i]:
        value |= 1 << i
    return value

