import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

display = Adafruit_SSD1306.SSD1306_128_64(rst=0)
display.begin()
display.clear()
display.display()
width = display.width
height = display.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    display.clear()
    display.display()
    draw.text((0, 5), u"T 25.7 \u00b0C", font=font, fill=255)
    draw.text((0, 35), "H 44%",  font=font, fill=255)
    display.image(image)
    display.display()
    time.sleep(2)
    display.image(Image.open('night_128x64.png').convert('1'))
    display.display()
    time.sleep(5)
