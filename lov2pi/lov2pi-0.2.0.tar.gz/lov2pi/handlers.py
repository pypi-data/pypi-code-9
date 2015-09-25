import subprocess
#import RPi.GPIO as GPIO


#GPIO.setup(led, GPIO.OUT)
# GPIO.output(led, 1) // or 0

def gpio_handler(data):
    #GPIO.setmode(GPIO.BCM)
    if data['command'] == 'set_direction':
        print data['direction']
        print data['pin']
       # GPIO.setup(data['pin'], GPIO.OUT if data['direction'] == 'out' else GPIO.IN )
        return 'ok'
    elif data['command'] == 'read_value':
        print data['pin']
    elif data['command'] == 'set_value':
        print data['pin']
        print data['value']
    else:
        return 'error'

def pwm_handler(command):
    print command

def camera_handler(command):
    print command

def ssh_handler(data):
    return subprocess.check_output(data['command'], shell=True)



