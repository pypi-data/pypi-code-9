"""
 MLX90614_test.py 
 Alexander Hiam <alex@graycat.io> 
 
 An example to demonstrate the use of the MLX90614 library included 
 with PyBBIO. Interfaces with the MLX90614 I2C non-contact IR thermometer.
 
 This example program is in the public domain.
"""

from bbio import *
# Import the MLX90614 class from the MLX90614 library:
from bbio.libraries.MLX90614 import MLX90614


# Initialize the I2C port the MLX90614 is attached to:
I2C2.open()
# Initialize the MLX90614:
ir_thermometer = MLX90614(I2C2)

def setup():
  pass

def loop():
  ambient_temp = ir_thermometer.readAmbientTempC()
  object_temp = ir_thermometer.readObjectTempC()

  print "ambient = {:0.2f} C - object = {:0.2f} C".format(
          ambient_temp,
          object_temp
          )
  delay(500)

run(setup, loop)