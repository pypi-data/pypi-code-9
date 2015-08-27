""" Driver for Newport's ESP (and others) motion controller and stages. 
  
  Usage:
  >>> esp = NewportESP('/dev/ttyUSB0') # open communication with controller
  >>> stage = esp.axis(1)   # open axis no 1
  >>> stage.id
  >>> stage.move_to(1.2)

[Capitalised methods/properties are for backward compatibility only.]

v. 0.3 (27 August 2015): update all methods/properties names to lowercase.
Capitalised versions are still available for backward compatibility.
"""

import serial
from time import sleep
#from  matplotlib.cbook import Stack 

class NewportError(Exception):
  """Represents errors raised by the ESP controller."""
  # Error are in the form of 'code, timestamp, MESSAGE', eg: '0, 451322, NO ERROR DETECTED'
  def __init__(self, string):
    self._string = string
    split_string = string.split(',')
    code = split_string[0]
    if len(code) == 3:
      self.axis = code[0]
      self.code = code[1:]
    else:
      self.axis = None
      self.code = code
    self.code = split_string[0]
    self.timestamp = split_string[1][1:]
    self.message = split_string[2][1:]
    
  def __str__(self):
    if self.axis is not None:
      if_axis_specific = ' on axis ' + self.axis
    else:
      if_axis_specific = ''
    return self.message + if_axis_specific

def catch_error(func):
  """A decorator to read error messages after calling ESP functions."""
  def inner(*args, **kwargs):
    self = args[0]
    func(*args, **kwargs)
    self.write('TB?', axis="")
    error_string = self.read()
    if error_string[0] is not '0':
      self.abort()
      raise NewportError(error_string)
  return inner

class ESP(object):
  """ Driver for Newport's ESP (100/300) motion controller.
  
  Usage:
  >>> esp = NewportESP.ESP('/dev/ttyUSB0') # open communication with controller
  >>> stage = esp.axis(1)   # open axis no 1
  """
  def __init__(self, ser_port):
    self.ser = serial.Serial(port=ser_port,
			     baudrate=19200,
			     bytesize=8,
			     timeout=1,
			     parity='N',
			     rtscts=1)
    print("Found controller: " + self.version)
    self.Abort = self.abort
    
  def __del__(self):
    self.ser.close()

  def read(self):
    """ Serial read with EOL character removed. """
    str = self.ser.readline()
    return str[0:-2]

  def write(self, string, axis = ""):
    """ Serial write() with EOL character appended, and axis ID if required """
    self.ser.write(str(axis) + string + "\r")
  
  @property
  def version(self):
    self.write("VE?")
    return self.read()

  def abort(self):
    self.write('AB', axis = "")

  def read_error(self):
    self.write('TB?')
    return self.read()
    
  def axis(self, axis_id):
    """Return an Axis object bound to the specified axis_id."""
    return Axis(self, axis=axis_id)

class Axis(object):
  """ Represents a Newport actuator or motorised stage attached to the ESP controller.
  
  Usage:
  >>> esp = NewportESP.ESP('/dev/ttyUSB0') # open communication with controller
  >>> stage = NewportESP.Axis(esp, axis = 1)   # open axis no 1
  """
  def __init__(self, controller, axis=1):
    self.axis = axis
    self.esp = controller
    self.read = self.esp.read
    print("Found motorised actuator: " + self.id)
    self.step_size_list = (1, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001)
    self.step_size = 6  # default increment for gotoRel (index in step_size_list)
    self.polling_time = 0.02
    
    self.HomeDefine = self.home_define
    self.HomeSearch = self.home_search
    self.PowerOff = self.off
    self.PowerOn = self.on
    self.GoToAbs = self.move_to
    self.GoToRel = self.move_by
    self.MoveUp = self.move_up
    self.MoveDown = self.move_down
    self.GoToTravelLimit = self.move_to_limit
    self.Stop = self.stop
    self.Abort = self.esp.abort
    self.abort = self.esp.abort
    self.WaitForMotionDone = self.wait
  
  def __del__(self):
    self.PowerOff()
  
  def write(self, string, axis = None):
    """ Send command string to axis (do not include axis number or EOL caracter)
    
    Can be used to send commands that are not covered by class methods
    """
    if axis == None:
      axis = self.axis
    # optional argument allows none-axis-specific commands
    # (most of which should be in the controller class, but a few are useful here.)
    self.esp.write(string, axis)    
  
  @property
  def id(self):
    self.write("ID?")
    return self.read()
  
  def on(self):
    self.write("MO")
    
  def off(self):
    self.write("MF")
    
  #def power(self, status=None):
  #  if status is None:
  #    self.write('MO?')
  #    return self.read() == '1'
  #  elif status is 

  def home_search(self, mode=0):
    self.write('OR'+str(mode))

  def home_define(self, pos0='?'):
    self.write('DH'+str(pos0))
    if pos0 == '?':
      return float(self.read())
    else:
      return pos0
  
  @property
  def moving(self):
    """ Returns True is motion is finished"""
    self.write("MD?")
    ret = self.read()
    if ret == "1":
      return False
    else:
      return True

  @property
  def isMotionDone(self):
    return (not self.moving)
      
  def wait(self):
    """Returns only after current motion is finished."""
    while self.moving:
      sleep(self.polling_time)
  
  @catch_error
  def move_to(self, pos, wait=False): 
    """Go to absolute position."""
    self.write("PA" + str(pos))
    if wait:
      self.WaitForMotionDone()

  @catch_error
  def move_by(self, pos, wait=False):
    """Go to relative position."""
    self.write("PR" + str(pos))
    if wait:
      self.WaitForMotionDone()  
    
  @property
  def position(self):
    self.write("TP")
    pos = self.read()
    return float(pos)
    
  def move_to_limit(self, direction):
    self.write('MT'+str(direction))
    
  def move_up(self):
    if self.isMotionDone:
      self.write('MV-')
    else:
      print("Previous motion is not done!")
        
  def move_down(self):
    if self.isMotionDone:
      self.write('MV+')
    else:
      print("Previous motion is not done!")
      
  def stop(self):
    self.write('ST')
  
  # What follows allows the user to call axis.StepUp/Down() to move the stage by a predermined amount
  # It's mostly useful with the GUI keypad, although it's simpler to 
  # implement at the GUI level with matplotlib.cbook.Stack, and will likely be removed in future versions.
    
  def stepUp(self, step = 0):
    """ Move up by a fixed increment. If the increment is not 
    specified, use the current default in step_size. """
    if step == 0: # no value given, use current default
      self.GoToRel(-self.currentStepSize)
    else:
      self.GoToRel(-step)

  def stepDown(self, step = 0):
    """ Move down by a fixed increment. If the increment is not 
    specified, use the current default in step_size. """
    if step == 0: # no value given, use current default
      self.GoToRel(+self.currentStepSize)
    else:
      self.GoToRel(+step)
  
  @property
  def currentStepSize(self):
    return self.step_size_list[self.step_size]
     
  def increaseStep(self):
    if self.step_size > 0:   # do nothing if already using the biggest step size
      self.step_size -= 1
      #print("Step size increased to " + str(self.step_size_list[self.step_size]) + 'mm.' )
      
  def decreaseStep(self):  # do nothing if already using the smallest step size
    if self.step_size < len(self.step_size_list) - 1:
      self.step_size += 1
      #print("Step size decreased to " + str(self.step_size_list[self.step_size]) + 'mm.' )
  
  @property  
  def resolution(self):
    self.write('SU?')
    return float(self.read())
    
  @property
  def unit(self):
    self.write('SN?')
    return UNIT[int(self.read())]
  
  def travel_limits(self, left=None, right=None):
    """Set or query the axis travel limits.
    
    **kwargs: - left, right:  Specifies the left/right travel limits.
                If none are provided, returns the current setting.
    """
    if left is None and right is None:
      self.write('SL?')
      left_lim = float(self.read())
      self.write('SR?')
      right_lim = float(self.read())
      return {'left': left_lim, 'right': right_lim}
    if left is not None:
      self.write('SL'+str(left))
    if right is not None:
      self.write('SR'+str(right))
  
  #def setVelocity(self, vel):

UNIT = {0: 'encoder count', 1: 'motor step', 2: 'millimiter', 3: 'micrometer',
4: 'inches', 5: 'milli-inches', 6: 'micro-inches', 7: 'degree', 8: 'gradient',
9: 'radian', 10: 'milliradian', 11: 'microradian'}
