from threading import Thread, Lock
import asyncio
from time import sleep, time
from websockets.server import serve
import json
from bless import (  
        BlessServer,
        BlessGATTCharacteristic,
        GATTCharacteristicProperties,
        GATTAttributePermissions
        )
from obd_data import speed, rpm, engine_load, throttle
from emulator import OBDSimulator
from config import read_config

obd_data = {
        speed: "",
        rpm: "",
        engine_load: "",
        throttle: ""
}

def simulate_data(lock):
    obd_sim = OBDSimulator()
    while True:
        obd_data = obd_sim.getValue()
        sleep(2)

    return

def gatt_server(lock, loop):
    config = read_config()
    #obd_service = "af7cf399-7046-4869-86e2-9aad105cc5ae"
    obd_service = config["obd_service_uuid"]

    characteristic_name_to_uuid = {
        speed: config["speed_characteristic_uuid"],
        rpm: config["rpm_characteristic_uuid"],
        engine_load: config["engine_load_characteristic_uuid"],
        throttle: config["throttle_characteristic_uuid"]
    }

    characteristic_uuid_to_name = {v: k for k, v in characteristic_name_to_uuid.items()}   

    gatt = {
       obd_service : {                                          
            characteristic_name_to_uuid[speed]: {
                "Properties": (GATTCharacteristicProperties.read |
                                   #GATTCharacteristicProperties.write |
                                   GATTCharacteristicProperties.indicate),
                "Permissions": (GATTAttributePermissions.readable
                                    # | GATTAttributePermissions.writeable
                                    ),
                "Value": None 
            },
            characteristic_name_to_uuid[rpm]: {
                "Properties": (GATTCharacteristicProperties.read |
                                   #GATTCharacteristicProperties.write |
                                   GATTCharacteristicProperties.indicate),
                "Permissions": (GATTAttributePermissions.readable
                                    # | GATTAttributePermissions.writeable
                                    ),
                "Value": None 
            },
            characteristic_name_to_uuid[engine_load]: {
                "Properties": (GATTCharacteristicProperties.read |
                                   #GATTCharacteristicProperties.write |
                                   GATTCharacteristicProperties.indicate),
                "Permissions": (GATTAttributePermissions.readable
                                    # | GATTAttributePermissions.writeable
                                    ),
                "Value": None 
            },
            characteristic_name_to_uuid[throttle]: {
                "Properties": (GATTCharacteristicProperties.read |
                                   #GATTCharacteristicProperties.write |
                                   GATTCharacteristicProperties.indicate),
                "Permissions": (GATTAttributePermissions.readable
                                    # | GATTAttributePermissions.writeable
                                    ),
                "Value": None 
            }
        },
    }

    def read_request(characteristic):
        # str(characteristic) is like: "51ff12bb-3ed8-46e5-b4f9-d64e2fec021b: Unknown"
        characteristic_name = characteristic_uuid_to_name[str(characteristic).split(":")[0].lower()]
        value = obd_data[characteristic_name]
        data_to_send = str(time()) + "--" + str(value)
        return bytearray(str(data_to_send).encode())

    async def run(loop):
        server = BlessServer(name="obd simulator", loop=loop)
        server.read_request_func = read_request

        await server.add_gatt(gatt)
        await server.start()
    
        while True:
            server.read_request(characteristic_name_to_uuid[speed]) # it does not matter here which characteristic you specify
            await asyncio.sleep(2)


    loop.run_until_complete(run(loop))

def ws_server(lock, address, port):
    async def send_data(websocket):
        while True:
            data_to_send = obd_data.copy()
            data_to_send["timestamp"] = time()
            json_result = json.dumps(data_to_send)
            await websocket.send(json_result)
            sleep(2)

    async def ws():
        async with serve(send_data, address, port):
            await asyncio.Future()  

    asyncio.run(ws())


loop = asyncio.get_event_loop()

config = read_config()

lock = Lock()
simulator_thread = Thread(target=simulate_data, args=(lock,))
gatt_client_thread = Thread(target=gatt_server, args=(lock,loop))
ws_server_thread = Thread(target=ws_server, args=(lock, config["ws_ip_addr"], config["ws_port"]))

simulator_thread.start()
gatt_client_thread.start()
ws_server_thread.start()

# end with ctrl+c

