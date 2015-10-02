__author__ = 'cristi'
#!/usr/bin/env python

from devicehub.devicehub import Sensor, Actuator, Device, Project

import threading

from time import sleep

import RPi.GPIO as GPIO

import json

import grovepi

PROJECT_ID     = '5408'  #projekct_id

DEVICE_UUID    = 'a524cca8-c279-4e81-a23d-a892d991ab76' #device_uuid

API_KEY        = '3cf4b512-c6c0-447e-bf6e-0097f183a4ab' #api_key

ACTUATOR_NAME1 = 'do_button' #do_button

# init pin

button = 2

relay = 4

led = 3

buzzer = 8

grovepi.pinMode(button,"INPUT")

grovepi.pinMode(relay,"OUTPUT")

grovepi.pinMode(buzzer,"OUTPUT")

grovepi.pinMode(led,"OUTPUT")

def switchRelay(state):

    if state == 1:

        grovepi.digitalWrite(relay,1)

        grovepi.digitalWrite(buzzer,1)

        sleep(1)

        grovepi.digitalWrite(relay,0)

        grovepi.digitalWrite(buzzer,0)

        grovepi.digitalWrite(led,1)     # Send HIGH to switch on LED

        sleep(1)

        grovepi.digitalWrite(led,0)     # Send LOW to switch off LED

        sleep(1)

    else:

        grovepi.digitalWrite(relay,0)

        sleep(.05)

    print "PIN ", relay, " state: ", state



def act1_callback(payload):

    """

    :param payload: payload sent to actuator

    """

    # handles message arrived on subscribed topic

    msg = str(payload)

    act_state = ACT1.state

    print "act1", act_state

    switchRelay(act_state)

project = Project(PROJECT_ID)

device = Device(project, DEVICE_UUID, API_KEY)

ACT1 = Actuator(Actuator.DIGITAL, ACTUATOR_NAME1)

device.addActuator(ACT1, act1_callback)

try:

    while True:

        pass

except KeyboardInterrupt:

    GPIO.cleanup()