"""
Author:             Ethan Scott
Date Created:       3/19/2024
Last Editted:       4/3/2024

Purpose:            This file contains the code to eject a USB drive plugged into the
                    Raspberry Pi with the pressing of a button. Currently, the drive must
                    be named 'BEAMdrive'. It does so through the use of the RPi.GPIO Python
                    module and a button connected to GPIO 27 and GND.

Sample Input:       python3 BEAMdrive_eject.py

Sample Output:      Press the button to eject the drive (Ctrl+C to exit)
                    Button pressed!
                    Drive has been unmounted and ejected.
                    Exiting.

NOTE:               - Coded in Python 3.12
                    - Please PIP INSTALL RPi.GPIO for python3. It is required to run this code.
                    - USB drive to be unmounted must be named 'BEAMdrive'. This means the code
                        will not allow the unmounting of any other connected USB devices.
                    - Only one USB drive may be connected at a time.
                    - There is currently no way to handle button presses when no drive is connected
                    - Needs to be integrated with BEAMweatherLightSensors.py

Sources:            - https://pypi.org/project/RPi.GPIO/
"""
import os
import RPi.GPIO as GPIO
import time

def eject_BEAMdrive():
    """_summary_
    Function to unmount and eject the current USB drive named 'BEAMdrive' connected.
    """
    unmountCMD = 'sudo umount /media/pi/BEAMdrive'
    ejectCMD = 'sudo eject /dev/sda1'
    os.system(unmountCMD)
    os.system(ejectCMD)
    print('Drive has been unmounted and ejected.')
    
def button_callback(channel):
    """_summary_
    Function to go about ejecting the USB drive with the press of a GPIO button.
    
    Args:
        channel (event): Button press.
    """
    print("Button pressed!")
    eject_BEAMdrive()

# Set up button to work with required fields. GPIO 27 pin used.
GPIO.setmode(GPIO.BCM)
button_pin = 27
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Set up event to be handled on button press
GPIO.add_event_detect(button_pin, GPIO.FALLING, callback = button_callback, bouncetime = 300)

# Constant loop to check for button presses
try:
    print("Press the button to eject the drive (Ctrl+C to exit)")
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting.")
    GPIO.cleanup()
# End file
