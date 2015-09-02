#!/bin/python

import ConfigParser
import logging
import time
import os
import signal
import sys
import RPi.GPIO as GPIO

from boxup_types import Colorcodes
# load visualization
from boxup_bicolormatrix import BicolorMatrixVisualization
from boxup_weatherradar import WeatherMatrixData
from boxup_gmailunread import GmailunreadMatrixData


config = ConfigParser.ConfigParser()
config.read('/etc/boxup/boxup_core.cfg')

logging.basicConfig(level=getattr(logging,config.get('Settings','LOGLEVEL'),None))
logger = logging.getLogger("boxup_core")
logger.info("Reading config-file...")

GPIO_RIGHT = config.getint('GPIO','RIGHT')
GPIO_LEFT = config.getint('GPIO','LEFT')
GPIO_LED_RIGHT = config.getint('GPIO','LED_RIGHT')
GPIO_LED_LEFT = config.getint('GPIO','LED_LEFT')
GPIO_ON = config.getint('GPIO','ON')
GPIO_OFF = config.getint('GPIO','OFF')

logger.info("Setup gpio...")
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_RIGHT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_LED_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_LED_LEFT, GPIO.OUT)
GPIO.setup(GPIO_ON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_OFF, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

ON = GPIO.HIGH
OFF = GPIO.LOW

data1 = [[-1 for x in range(8)] for y in range(8)]
data2 = [[-1 for x in range(8)] for y in range(8)]
matrix = BicolorMatrixVisualization()
datamatrix1 = WeatherMatrixData()
datamatrix2 = GmailunreadMatrixData()

def updateView(event):
	logger.info("Event occured: "+str(event))
	logger.info("Starting run...")
	time.sleep(0.2)
	if(GPIO.input(GPIO_ON)):
		logger.info("Is on!")
	elif(GPIO.input(GPIO_OFF)):
		logger.info("Is off!")
		GPIO.output(GPIO_LED_RIGHT, OFF)
		GPIO.output(GPIO_LED_LEFT, OFF)
		matrix.clear()
		return
	else:
		logger.warn("Impossible state! If not on, nor off!")
	
	
	isRight = False
	logger.info("Setting leds, in addition to switch state...")
	if(GPIO.input(GPIO_RIGHT)):
		isRight = True
		logger.info("Is right!")
	elif(GPIO.input(GPIO_LEFT)):
		isRight = False
		logger.info("Is left!")
	else:
		logger.warn("Impossible state! If not right, nor left!")
	
	if(isRight):
		GPIO.output(GPIO_LED_RIGHT, ON)
		GPIO.output(GPIO_LED_LEFT, OFF)
		for x in range(8):
			for y in range(8):
				matrix.setPx(x,y,data1[x][y])
		matrix.update()
		
	else:
		GPIO.output(GPIO_LED_LEFT, ON)
		GPIO.output(GPIO_LED_RIGHT, OFF)
		for x in range(8):
			for y in range(8):
				matrix.setPx(x,y,data2[x][y])
		matrix.update()

	

def updateData():
	for x in range(8):
		for y in range(8):
			data1[x][y] = datamatrix1.getPx(x,y)
			logger.info("field1: "+str(data1[x][y]))
			data2[x][y] = datamatrix2.getPx(x,y)
			logger.info("field2: "+str(data2[x][y]))


def start():
	GPIO.add_event_detect(GPIO_RIGHT, GPIO.RISING, callback=updateView, bouncetime=300)
	GPIO.add_event_detect(GPIO_LEFT, GPIO.RISING, callback=updateView, bouncetime=300)
	GPIO.add_event_detect(GPIO_ON, GPIO.RISING, callback=updateView, bouncetime=300)
	GPIO.add_event_detect(GPIO_OFF, GPIO.RISING, callback=updateView, bouncetime=300)
	try:
		while (True):
			updateData()	
			updateView("no event")
			time.sleep(30)
	except KeyboardInterrupt:
		logger.info("Programm canceled. Finishing")
	finally:
		GPIO.cleanup()
		matrix.clear()

def signal_handler(signal, frame):
	logger.info('SIGINT or SIGTERM recieved. finishing...')
	GPIO.cleanup()
	matrix.clear()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)




if __name__ == "__main__":
	start()
else:
	logger.warning("run this module as __main__!")
	GPIO.cleanup()
	matrix.clear()
