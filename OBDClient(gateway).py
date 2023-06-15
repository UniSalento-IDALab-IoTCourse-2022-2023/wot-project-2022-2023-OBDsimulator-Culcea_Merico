#!/bin/python3

'''
/home/kynesys/.local/lib/python3.10/site-packages/pint/compat/__init__.py - riga 64
    ho cambiato import Chainmap in import ChainMap
 
/home/kynesys/.local/lib/python3.10/site-packages/pint/util.py - riga 21
    ho cambiato from collections -> from collections.abc
'''

import obd
import time

def get_speed():
    connection = obd.OBD("/dev/pts/4")  # Connect to OBD-II device over Bluetooth
    cmd = obd.commands.SPEED  # Speed command
    response = connection.query(cmd)  # Send command and receive response

    if response.is_null():
        print("No speed data received.")
    else:
        speed = response.value.magnitude  # Get the speed value
        print(f"Current speed: {speed} km/h")

    connection.close()  # Close the connection

while True:
    time.sleep(1)
    get_speed()
