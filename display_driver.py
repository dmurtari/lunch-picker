#!/usr/bin/python

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import restaurants
import Image
import ImageDraw
import ImageFont
import RPi.GPIO as GPIO
import time

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0
PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def show_lunch():
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE,\
                                               max_speed_hz=4000000))
    disp.begin(contrast=60)
    font = ImageFont.load_default()

    restaurant = restaurants.pick_restaurant()
    name = restaurant["name"]
    price = '$' * restaurant["price"]
    cuisines = restaurant["cuisines"].split(",")[0]
    address = restaurant["address"].split(",")[0]
    if restaurant["rating"] == "0":
        rating = "No ratings"
    else:
        rating = restaurant["rating"] + "/5"

    x = 0
    max_x = max(len(name), len(cuisines), len(address)) * 6 - LCD.LCDWIDTH
    iterations = 0

    while True:
        disp.clear()
        disp.display()

        image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0 ,LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
        time.sleep(0.1)

        draw.text((x,0), 'Go Eat At:', font=font)
        draw.text((x,9), name, font=font)
        draw.text((x,18), cuisines, font=font)
        draw.text((x,27), address, font=font)
        draw.text((x,36), rating + ' (' + price + ')', font=font)

        disp.image(image)
        disp.display()

        if iterations > 1:
            break

        if x == 0:
            time.sleep(2)
        else:
            time.sleep(0.1)

        state = GPIO.input(PIN)
        if state == False:
            break

        if x < -max_x:
            x = 0
            time.sleep(1)
            iterations += 1
        else:
            x -= 3

    return

if __name__ == "__main__":
    show_lunch()
