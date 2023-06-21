#!/bin/python3

import socket
import time
import json
client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

client.connect(("E4:5F:01:5F:5C:35", 4))
print("Client connected...")

try:
    while True:
        message = client.recv(1024)
        if not message: 
                    break
        print("Message received: {}".format(json.loads(message)))
except OSError as e:
    pass

client.close()
