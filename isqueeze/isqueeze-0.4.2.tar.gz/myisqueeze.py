#!/usr/bin/env python
# -*- coding:utf-8 -*


import sys
sys.path.insert(0,'../../FGPIO')#Pour travailler sur les sources
sys.path.insert(0,'../../FAVRIP')
sys.path.insert(0,'../../FUTIL')

from isqueeze import *
from FAVRIP.denon import *
from FGPIO.rpiduino_io import *
from FGPIO.lcd_i2c_io import *
from FGPIO.bt_io import *
from FGPIO.rotary_encoder_io import *
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

logging.info("isqueeze start now")

pc = rpiduino_io()

if isinstance(pc, pcduino_io): # Si c'est un pcduino
	lcd = lcd_i2c_io(bus=2,addr=0x27, pin_bl=pc.logical_pin(6), lines=2, width=16)
	#led = led_io(pc.logical_pin(2)) # led sur pin 2 arduino ou 13 Rpi (GPIO2)
	bt_onoff = bt_io(pc.logical_pin(3))# Bt on_off sur la pin 3 arduino ou GPIO3 du Rpi
	bt_playpause = bt_io(pc.logical_pin(4))
	bt_next = bt_io(pc.logical_pin(5))
	bt_rot = bt_rotatif_io(*pc.logical_pins(9,10,8), auto=True)
	#bt_rot = bt_pseudo_rotatif_io(*pc.logical_pins(10,9,8)) #pour test en émulant un bouton rotatif par 3 boutons
	# ext_io = mcp23017_io(addr=0x23, pc=pc)
	bts_preset=[]
	# bts_preset = [ \
		# bt_io(ext_io.pin[8]), \
		# bt_io(ext_io.pin[9]), \
		# bt_io(ext_io.pin[10]), \
		# bt_io(ext_io.pin[11]), \
		# bt_io(ext_io.pin[12]), \
		# bt_io(ext_io.pin[13]) \
		# ]
	infra_rouge = False
else: # Si c'est un Raspberry Pi
	lcd = lcd_i2c_io(pc=pc, pin_bl=pc.physical_pin(8), lines=4, width=20)
	#led = led_io(pc.physical_pin(21)) # led sur pin 2 arduino ou 13 Rpi (GPIO2)
	bt_onoff = bt_io(pc.physical_pin(11)) # Bt on_off sur la pin 3 arduino ou GPIO3 du Rpi
	bt_playpause = bt_io(pc.physical_pin(13))
	bt_next = bt_io(pc.physical_pin(15))
	bt_rot = bt_rotatif_io(*pc.physical_pins(18,16,7), auto=True)
	bts_preset = [ \
		bt_io(pc.physical_pin(26)), \
		bt_io(pc.physical_pin(24)), \
		bt_io(pc.physical_pin(23)), \
		bt_io(pc.physical_pin(22)), \
		bt_io(pc.physical_pin(21)), \
		bt_io(pc.physical_pin(19)) \
		]
	infra_rouge = True
	
myisqueeze = isqueeze( \
				SB_serveur_ip = '192.168.10.10', \
				SB_client_name = 'PISALON', \
				ampli = denonAVR('192.168.10.11'), \
				ampli_input = 'aux2',\
				lcd = lcd, \
				bt_onoff = bt_onoff, \
				bt_playpause = bt_playpause, \
				bt_next = bt_next, \
				bt_rot = bt_rot, \
				bts_preset = bts_preset, \
				infra_rouge = infra_rouge)

myisqueeze.wait_ctrl_c()