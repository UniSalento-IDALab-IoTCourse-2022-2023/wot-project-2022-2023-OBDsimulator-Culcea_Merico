#!/bin/python3

'''
    CAMBIARE __device con il device su cui runna l'emulatore OBD ircama
'''


import socket
import obd
import json
from datetime import datetime
import time

class OBDClient():
    __device = "/dev/pts/1"
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
            "timestamp" : timestamp,
            "speed" : speed,
            "rpm" : rpm,
            "engineLoad" : engineLoad,
            "throttle" : throttle
        }
        return json.dumps(data)

class BleOBD_emulator():
    __bleAddress = "E4:5F:01:5F:5C:35" # linux 00:F4:8D:74:36:12 rasp E4:5F:01:5F:5C:35
    __bleChannel = 4
    __socketInstance = None
    __clientAddress = None
    __clientSocket = None

    def __init__(self):
        self.__socketInstance = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.__socketInstance.bind((self.__bleAddress, self.__bleChannel))
        self.__socketInstance.listen(1)
        print("Ble Server ready to listen...") 

    def waitForConnection(self):
        print("Ble Server waiting for client...")
        self.__clientSocket, self.__clientAddress = self.__socketInstance.accept()
        print("Client connected - Address: {}".format(self.__clientAddress))

    def sendData(self):
        obdClient = OBDClient()
        try:
            while True:
                data = obdClient.getValue()
                self.__clientSocket.client.send(data.encode("utf-8"))
                print("Message sent: {}".format(data.decode("utf-8")))
                time.sleep(5)
        except OSError as e:
            pass
        self.__clientSocket.close()

    def getAddress(self):
        return self.bleAddress

    def getChannel(self):
        return self.bleChannel

    def serverShutdown(self):
        self.__socketInstance.close()

    def main(self):
        self.waitForConnection()
        self.sendData()
        self.shutdown()

if __name__ == "__main__":
    bleOBD_emulator = BleOBD_emulator()
    bleOBD_emulator.main()