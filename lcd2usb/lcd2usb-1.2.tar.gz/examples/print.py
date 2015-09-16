#!/usr/bin/env python
# encoding: utf8

'''print.py - print characters (0~255) one by one
'''

import time
from lcd2usb import LCD


def main(lcd):
    lcd.clear()
    i = 0
    while True:
        print i
        lcd.write(chr(i))
        i += 1
        if i > 255:
            i = 0
        time.sleep(0.1)

if __name__ == '__main__':
    lcd = LCD.find_or_die()
    lcd.info()
    try:
        main(lcd)
    except KeyboardInterrupt:
        pass
