#!/bin/python3

import socket
import obd
import json
# from datetime import datetime
from time import time
from config import read_config

# class OBDClient():
#     __device = "/dev/pts/3"
#     __emulatorInstance = None
#
#     def __init__(self):
#         self.__emulatorInstance = obd.OBD(self.__device)
#
#     def getValue(self):
#         timestamp = datetime.now()
#         speed = self.__emulatorInstance.query(obd.commands.SPEED)
#         engineLoad = self.__emulatorInstance.query(obd.commands.ENGINE_LOAD)
#         throttle = self.__emulatorInstance.query(obd.commands.THROTTLE_POS)
#         rpm = self.__emulatorInstance.query(obd.commands.RPM)
#
#         data = {
#             "timestamp" : str(timestamp),
#             "speed" : str(speed),
#             "rpm" : str(rpm),
#             "engineLoad" : str(engineLoad),
#             "throttle" : str(throttle)
#         }
#         return json.dumps(data)

class BleOBD_server():
    __bleChannel = 4
    __socketInstance = None
    __clientAddress = None
    __clientSocket = None

    def __init__(self):
        config = read_config()
        ble_address = config["raspberry_ble_addr"]
        self.__socketInstance = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.__socketInstance.bind((ble_address, self.__bleChannel))
        self.__socketInstance.listen(1)
        print("Ble Server ready to listen...")

    def waitForConnection(self):
        print("Ble Server waiting for client...")
        self.__clientSocket, self.__clientAddress = self.__socketInstance.accept()
        print("Client connected - Address: {}".format(self.__clientAddress))

    def sendData(self):
        emulator = OBDSimulator()
        try:
            while True:
                data = emulator.getValue()
                data["timestamp"] = time()
                self.__clientSocket.send(data.encode("utf-8"))
                print("Message sent: {}".format(data))
                time.sleep(5)
        except OSError as e:
            pass
        self.__clientSocket.close()

    def getChannel(self):
        return self.__bleChannel

    def serverShutdown(self):
        self.__socketInstance.close()

    def main(self):
        self.waitForConnection()
        self.sendData()
        self.shutdown()

if __name__ == "__main__":
    server = BleOBD_server()
    server.main()
