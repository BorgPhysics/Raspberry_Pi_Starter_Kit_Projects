#!/usr/bin/env python3
#############################################################################
# Filename    : Thermometer.py
# Description : DIY Thermometer
# Author      : www.freenove.com
# modification: 2019/03/09
########################################################################
import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
        
def loop():
    while True:
        value = adc.analogRead(0)        # read ADC value A0 pin
        voltage = value / 255.0 * 3.3        # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
        # 1 / ( 0.00335401643468052993459667952373 + log(Rt/10)/3950 )
        tempK = 1/  (1 /(273.15 + 25) + math.log(Rt/10) / 25000.0) # calculate temperature (Kelvin)
        #tempK = 1/  (1 /(273.15 + 25) + math.log(Rt/10) / 3950.0) # calculate temperature (Kelvin)
        tempC = tempK -273.15        # calculate temperature (Celsius)
        tempF = tempC * 9/5 + 32        # calculate temperature (Fahrenheit)
        #print ('ADC Value : %d, Voltage : %.2f, Temperature : %.2f'%(value,voltage,tempC))
        print ('ADC Value : %d, Volts : %.2f, Ohms : %.2f, Temp C : %.2f, Temp F : %.2f'%(value, voltage, Rt, tempC, tempF))
        time.sleep(0.01)

def destroy():
    adc.close()
    GPIO.cleanup()
    
if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
        
