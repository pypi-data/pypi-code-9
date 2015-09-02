import ConfigParser
import logging

from Adafruit_LED_Backpack import BicolorMatrix8x8
from boxup_types import MatrixVisualization
from boxup_types import Colorcodes

logger = logging.getLogger("boxup_bicolormatrix")
logger.info("Reading config-file...")

config = ConfigParser.ConfigParser()
config.read('/etc/boxup/plugins/boxup_bicolormatrix.cfg')

BRIGHTNESS = config.getint('Settings','BRIGHTNESS')


class BicolorMatrixVisualization (MatrixVisualization):
	__matrix = [[-1 for x in range(8)] for y in range(8)]
	def getWidth(self):
		return 8
	def getHeight(self):
		return 8
	def setPx(self,x,y,color):
		self.__matrix[x][y] = color	
	def update(self):
		logger.info("Opening display...")
		display = BicolorMatrix8x8.BicolorMatrix8x8()
		display.begin()
		display.set_brightness(BRIGHTNESS)
		
		for x in range(8):
			for y in range(8):
				try:
					c = self.__matrix[x][y]
					if c == Colorcodes.GREEN:
						c = BicolorMatrix8x8.GREEN
					elif c == Colorcodes.ORANGE:
						c = BicolorMatrix8x8.YELLOW
					elif c == Colorcodes.RED:
						c = BicolorMatrix8x8.RED
					elif c == Colorcodes.OFF:
						c = 0
					else:
						logging.warning("Unhandeld color value: "+c)
					display.set_pixel(x,y,c)
				except:
					logger.error("error by updating matrix")
					display.set_pixel(x,y,0)
		logger.info("Writing to display...")
		display.write_display()
	def clear(self):
		logger.info("Opening display...")
		display = BicolorMatrix8x8.BicolorMatrix8x8()
		display.begin()
		display.set_brightness(BRIGHTNESS)
		for x in range(8):
			for y in range(8):
				display.set_pixel(x,y,0)
		logger.info("Writing to display...")
		display.write_display()
		

# Check if module is running as __main__
if __name__ == "__main__":
    logger.error("Can not run this script as __main__. Use it as Module for boxup.")

    
