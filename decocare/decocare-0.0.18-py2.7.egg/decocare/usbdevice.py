
class ID:
  VENDOR  = 0x0a21
  PRODUCT = 0x8001

import usb.core
import usb.util
import platform
def scan ( ):
  dev = usb.core.find(idVendor=ID.VENDOR)
  return dev

class UsbLink (object):
  touches_kernel = False
  def __init__(self, dev):
    self.dev = dev
  def configure (self):
    if self.dev:
      cfg =  self.dev.get_active_configuration( )
      self.interface = cfg[(0,0)]
      print self.interface
      self.OUT = usb.util.find_descriptor(self.interface, custom_match = \
        lambda e: \
          usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
      print "OUT"
      print self.OUT
      self.IN = usb.util.find_descriptor(self.interface, custom_match = \
        lambda e: \
          usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
      print "IN"
      print self.IN
      if platform.system( ) not in ['Windows']:
        self.touches_kernel = True
        self.dev.detach_kernel_driver(1)
      """
      """
      usb.util.claim_interface(self.dev, self.interface)
  def close (self):
    usb.util.dispose_resources(self.dev)
    if self.touches_kernel:
      self.dev.attach_kernel_driver(self.interface)
  def read (self, n):
    return bytearray(self.ep.read(n))
  def write (self, msg):
    return self.OUT.write(msg)

if __name__ == '__main__':
  dev = scan( )
  print dev
  link = UsbLink(dev)
  link.configure( )
  link.close( )

