
import obd
import json
from datetime import datetime
from time import sleep


class OBDClient():
    __device = "/dev/pts/3"
    __emulatorInstance = None

    def __init__(self):
        self.__emulatorInstance = obd.OBD(self.__device)

    def getValue(self):
        timestamp = datetime.now()
        speed = self.__emulatorInstance.query(obd.commands.SPEED)
        engineLoad = self.__emulatorInstance.query(obd.commands.ENGINE_LOAD)
        throttle = self.__emulatorInstance.query(obd.commands.THROTTLE_POS)
        rpm = self.__emulatorInstance.query(obd.commands.RPM)

        data = {
            "timestamp" : str(timestamp),
            "speed" : str(speed),
            "rpm" : str(rpm),
            "engineLoad" : str(engineLoad),
            "throttle" : str(throttle)
        }
        return json.dumps(data) 

obdf = OBDClient()
while True:
    print(obdf.getValue())
    sleep(1)
