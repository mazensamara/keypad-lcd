# for using a membrane keypad and i2c lcd with the Raspberry Pi 

# A module to control Raspberry Pi GPIO channels
# use the following command: pip install RPi.GPIO

# Define lcd (Need to install rpi_lcd on Raspberry pi)
# First Command: wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/lcd_i2c.py
# Second Command: sudo pip3 install rpi_lcd

import RPi.GPIO as GPIO
import time
from rpi_lcd import LCD

lcd = LCD()

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21


# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

input = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel
       
# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

# reads the columns and appends the value, that corresponds
# to the button, to a variable    
def readLine(line, characters):
    global input
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
        print(input)
        lcd.text(input, 1)       
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
        print(input)
        lcd.text(input, 1)              
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
        print(input)
        lcd.text(input, 1)              
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
        print(input)
        lcd.text(input, 1)
        lcd.text(input, 2)      
    GPIO.output(line, GPIO.LOW)

try:
    while True:  
        readLine(L1, ["1","2","3","+"])
        readLine(L2, ["4","5","6","-"])
        readLine(L3, ["7","8","9","*"])
        readLine(L4, ["=","0","CE","/"])
        time.sleep(0.2)
       
except KeyboardInterrupt:
    print("\nApplication stopped!")
    lcd.clear() 
    
    

    
