#!/usr/bin/python3

import restaurants
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
 
import Image
import ImageDraw
import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

def show_lunch():
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE,\
                                               max_speed_hz=4000000))
    disp.begin(contrast=45)
    
    # Clear display.
    disp.clear()
    disp.display()
    
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
     
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
     
    # Draw a white filled box to clear the image.
    draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    
    # Load default font.
    font = ImageFont.load_default()
     
    restaurant = restaurants.pick_restaurant()
    draw.text((0,0), 'GOTO (' + '$' * restaurant["price"] + ')', font=font)
    draw.text((0,10), restaurant["name"], font=font)
    draw.text((0,20), '(' + restaurant["cuisines"] +')', font=font)
    draw.text((0,30), restaurant["address"], font=font)
     
    # Display image.
    disp.image(image)
    disp.display()
    return

if __name__ == "__main__":
    show_lunch()        
