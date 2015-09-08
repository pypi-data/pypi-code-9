from time import sleep
from smbus import SMBus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
bus = 0

class PiTouch:

  def __init__(self):
    if GPIO.RPI_REVISION == 1: # Although PiTouch doesn't fit, keep for compatibility
      i2c_bus = 0
    elif GPIO.RPI_REVISION >= 2: # As well as the rev 2
      i2c_bus = 1
    else:
      print "Unable to determine Raspberry Pi revision."
      exit
  
    self.bus = SMBus(i2c_bus)
    self.bus.write_byte_data(0x40, 0x00, 0x10)
    self.bus.write_byte_data(0x40, 0xFE, 0x00)
    sleep(0.01)
    self.bus.write_byte_data(0x40, 0x00, 0x00)
    self.bus.write_byte_data(0x40, 0x01, 0x04)
    sleep(0.01)
    ## Fin init PCA

    GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)


  def brightness(self,input):
    if input == 0:
      return 4096
    else:
      return (input - 0) * (4094 - 0) // (100 - 0) + 1


  def light(self,chan,light):
    light = self.brightness(light)
    self.bus.write_byte_data(0x40, chan, light & 0xFF)
    self.bus.write_byte_data(0x40, chan+1, light >> 8)
    self.bus.write_byte_data(0x40, chan+2, 0 & 0xFF)
    self.bus.write_byte_data(0x40, chan+3, 0 >> 8)


  def red(self,light,pad=0):
    #3, 0, 10, 13
    if pad == 0:
      self.light(0x06+(4*3),light)
      self.light(0x06+(4*0),light)
      self.light(0x06+(4*10),light)
      self.light(0x06+(4*13),light)
    elif pad == 1:
      self.light(0x06+(4*3),light)
    elif pad == 2:
      self.light(0x06+(4*0),light)
    elif pad == 3:
      self.light(0x06+(4*10),light)
    elif pad == 4:
      self.light(0x06+(4*13),light)


  def green(self,light,pad=0):
    #4, 1, 11, 14
    if pad == 0:
      self.light(0x06+(4*4),light)
      self.light(0x06+(4*1),light)
      self.light(0x06+(4*11),light)
      self.light(0x06+(4*14),light)
    elif pad == 1:
      self.light(0x06+(4*4),light)
    elif pad == 2:
      self.light(0x06+(4*1),light)
    elif pad == 3:
      self.light(0x06+(4*11),light)
    elif pad == 4:
      self.light(0x06+(4*14),light)


  def blue(self,light,pad=0):
    #5, 2, 12, 15
    if pad == 0:
      self.light(0x06+(4*5),light)
      self.light(0x06+(4*2),light)
      self.light(0x06+(4*12),light)
      self.light(0x06+(4*15),light)
    elif pad == 1:
      self.light(0x06+(4*5),light)
    elif pad == 2:
      self.light(0x06+(4*2),light)
    elif pad == 3:
      self.light(0x06+(4*12),light)
    elif pad == 4:
      self.light(0x06+(4*15),light)


  def all(self,light):
    light = self.brightness(light)
    self.bus.write_byte_data(0x40, 0xFA, light & 0xFF)
    self.bus.write_byte_data(0x40, 0xFB, light >> 8)
    self.bus.write_byte_data(0x40, 0xFC, 0 & 0xFF)
    self.bus.write_byte_data(0x40, 0xFD, 0 >> 8)


  def read(self):
    readpad = self.bus.read_byte_data(0x1b, 0x03)
    if readpad == 8:
      return 1
    if readpad == 16:
      return 2
    if readpad == 4:
      return 3
    if readpad == 2:
      return 4

  def touch(self):
    while True:
      if GPIO.input(11) == 0:
        read = self.read()
        if 4 >= read > 0:
          return self.read()
