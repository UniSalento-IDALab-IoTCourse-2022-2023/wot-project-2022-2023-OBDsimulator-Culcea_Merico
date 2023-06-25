import obd
import json
from datetime import datetime
from time import sleep
from obd_data import speed, rpm, engine_load, throttle
from config import read_config

class OBDSimulator():
    __emulatorInstance = None

    def __init__(self):
        config = read_config()

        #device = "/dev/pts/3"
        device = config["emulator_pseudotty"]
        self.__emulatorInstance = obd.OBD(device)

    def getValue(self):
        timestamp = datetime.now()
        speed_value = self.__emulatorInstance.query(obd.commands.SPEED)
        engine_load_value = self.__emulatorInstance.query(obd.commands.ENGINE_LOAD)
        throttle_value = self.__emulatorInstance.query(obd.commands.THROTTLE_POS)
        rpm_value = self.__emulatorInstance.query(obd.commands.RPM)

        data = {
            #"timestamp" : str(timestamp),
            speed : str(speed_value),
            rpm : str(rpm_value),
            engine_load : str(engine_load_value),
            throttle : str(throttle_value)
        }
        return data 
