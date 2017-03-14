#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import display_driver

PIN = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(PIN)
    if state == False:
        print('Button pushed')
        display_driver.show_lunch()
        time.sleep(0.2)
