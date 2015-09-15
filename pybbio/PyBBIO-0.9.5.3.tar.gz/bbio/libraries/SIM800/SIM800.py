


class SIM800(object):

  def __init__(self, serial_port):
    self.serial_port = serial_port


  def saveProfile(self):
    at_str = "AT&W"

  def readAT(self):
    at_str = "AT+{}?"

  def writeAT(self):
    at_str = "AT+{}={}"

  def testAT(self):
    at_str = "AT+{}=?"

  def executeAT(self):
    at_str = "AT+{}"

