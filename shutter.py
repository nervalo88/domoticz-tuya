#!/usr/bin/python3

import time
import sys

import tuya

if len(sys.argv) <= 1:
    print("not enough arguments")
    exit()

voletSalonClosed = False
voletSaMClosed = False
voletCuisineClosed = False

light = tuya.tuya_api("light")
voletSalon = tuya.tuya_api("voletSalonJardin")
voletSaM = tuya.tuya_api("voletSalonRue")
voletCuisine = tuya.tuya_api("voletCuisine")

if sys.argv[1] == 'open':
    voletSalon.moveShutter("open")
    voletSaM.moveShutter("open")
    voletCuisine.moveShutter("open")
elif sys.argv[1] == 'close':
    voletSalon.moveShutter("close")
    voletSaM.moveShutter("close")
    voletCuisine.moveShutter("close")
elif sys.argv[1] == 'stop':
    voletSalon.moveShutter("stop")
    voletSaM.moveShutter("stop")
    voletCuisine.moveShutter("stop")
elif sys.argv[1] == 'light':
    if sys.argv[2] == 'on':
        light.switchLed('true')
    elif sys.argv[2] == 'off':
        light.switchLed('false')
elif sys.argv[1] == 'sun':
    start_time = time.time()
    voletSalon.moveShutter("close")
    voletSaM.moveShutter("close")
    voletCuisine.moveShutter("close")
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 11.0 and not voletSalonClosed:
            voletSalon.moveShutter("stop")
            voletSalonClosed = True
        if elapsed_time >= 13.0 and not voletSaMClosed:
            voletSaM.moveShutter("stop")
            voletSaMClosed = True
        if elapsed_time >= 7.0 and not voletCuisineClosed:
            voletCuisine.moveShutter("stop")
            voletCuisineClosed = True
        if voletSalonClosed and voletSaMClosed and voletCuisineClosed:
            break
        time.sleep(0.5)

