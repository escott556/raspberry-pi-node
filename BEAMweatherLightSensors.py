"""
Author:             Ethan Scott
Date Created:       2/13/2024
Last Editted:       4/3/2024

Purpose:            This file contains the code to run the BME-280 weather sensor and
                    the TSL-2561 light sensor through the use of i2c and SPI
                    communication, respectively, with a Raspberry Pi. After data is 
                    collected from the sensors, it is sent (appended) to a JSON file
                    also found on the Pi.

Sample Input:       python3 BEAMweatherLightSensors.py

Sample Output:      Entering loop
                    Sample 1
                    Time: 12:00:00 EST
                    Temp: 23.739 oC
                    Humidity: 43.965 %rH
                    Pressure: 1019.2 hPa
                    Enabled
                    Gain = ... (varies)
                    Integration time = ... (varies)
                    Broadband = 3.860
                    Infrared = 0
                    Keyboard interruption: Program stopped!

NOTE:               - Note GPIO layout of Pi and ensure sensors wired correctly.
                    - Coded in Python 3.12
                    - Please PIP INSTALL related libraries:
                        adafruit-circuitpython-bme280
                        adafruit-circuitpython-tsl2561
                    - Only one i2c device available on-board on GPIO at a time
                        (can be extended with an i2c MUX, added costs).
                        This code only accounts for one i2c device
                    - Formatting of JSON data can be adjusted.
                    - Needs to be integrated with BEAMejectDrive.py

Sources             - https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/downloads
                    - https://learn.adafruit.com/tsl2561/python-circuitpython

"""
import json
import time
from datetime import datetime
from datetime import date
import board
import digitalio
import busio
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_tsl2561

# Create the I2C bus and initializing the TSL-2561
i2c = busio.I2C(board.SCL, board.SDA)
tsl2561 = adafruit_tsl2561.TSL2561(i2c)
time.sleep(1)
tsl2561.gain = 0                            # Set gain 0=1x, 1=16x
tsl2561.integration_time = 1                # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)

# Create SPI connection and initializing the BME-280
spi = board.SPI()
bme_cs = digitalio.DigitalInOut(board.D25)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)
bme280.sea_level_pressure = 1013.25

# Looping until stopped, 5 second sample rate (adjustable)
print ('Entering loop')
running = True
sampleCount = 0
while running:
    try:
        sampleCount += 1
        print ('Sample ' + str(sampleCount))

        # Getting BME-280 sensor data
        temp_oC = str(bme280.temperature)
        humidity = str(bme280.humidity)
        pressure = str(bme280.pressure)
        altitude = str(bme280.altitude)
        temp_oC = str(round(bme280.temperature, 3))
        humidity = str(round(bme280.humidity, 3))
        pressure = str(round(bme280.pressure, 3))
        dateAndTime = str(datetime.now())[:-7]                  # -7 decimal places
        today = str(date.today())
        timeNow = str(datetime.time(datetime.now()))[:-7]

        tsl2561.enabled = True                                  # Enable the light sensor
        # Getting TSL-2561 sensor data
        broadband = str(tsl2561.broadband)
        infrared = str(tsl2561.infrared)
        lux = str(tsl2561.lux)
        lightLevel = None
        luminosity = str(tsl2561.luminosity)

        if lux is not None:                                     # Handle no light error
            lightLevel = str(lux)[:-7]
        else:
            print("Lux value error: May be over- or under-range.")

        # Getting sensor data and storing within a Python data dictionary (hash map)
        light_data = {
            str(today) : [
                {"time" : timeNow,
                "broadband" : broadband,
                "infrared" : infrared,
                "lightLevel" : lightLevel,
                "luminosity" : luminosity
                  }
            ]
        }
        weather_data = {
            str(today) : [
                {"time" : timeNow,
                "temp_oC" : temp_oC,
                "humidity" : humidity,
                "pressure" : pressure
                 }
            ]
        }

        # Dump/appending light data dictionary into JSON format and file
        with open(r'/home/pi/BEAM/sensor_data.json', 'a') as file:
            json.dump(light_data, file, indent = 4)

        # Dump/appending weather data dictionary into JSON format and file
        with open(r'/home/pi/BEAM/sensor_data.json', 'a') as file:
            json.dump(weather_data, file, indent = 4)

        # Test prints
        print('Time: ' + timeNow + ' EST')
        print('Temp: ' + temp_oC + ' oC')
        print('Humidity: ' + humidity +  ' %rH')
        print('Pressure: ' + pressure + ' hPa')
        print("Enabled = {}".format(tsl2561.enabled))
        print("Gain = {}".format(tsl2561.gain))
        print("Integration time = {}".format(tsl2561.integration_time))
        print("Broadband = {}".format(broadband))
        print("Infrared = {}".format(infrared))

        time.sleep(5)                                           # Sample delay: 5 seconds
    except KeyboardInterrupt:
        print('Keyboard interruption: Program stopped!')
        tsl2561.enabled = False                                 # Shut off Lux sensor
        running = False
    except Exception as e:
        print('Unexpected error: ', str(e))
        running = False\

print("Loop exited successfully.")
# End file
