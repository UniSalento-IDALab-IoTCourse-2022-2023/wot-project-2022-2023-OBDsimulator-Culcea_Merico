from threading import Thread, Lock
import asyncio
from time import sleep
from bless import (  
        BlessServer,
        BlessGATTCharacteristic,
        GATTCharacteristicProperties,
        GATTAttributePermissions
        )

# define an enum-like, to avoid typing the string explicitly
speed = "speed"
# ...

obd_data = {
        speed: -1,           
}

def simulate_data(lock):
    while True:
        # change obd_data based on the result of the simulator
        sleep(2)

    """example:
    counter = 0
    while True:
        obd_data[speed] = counter
        counter += 1
        sleep(2)
    """

    return

def gatt_server(lock, loop):
    obd_service = "af7cf399-7046-4869-86e2-9aad105cc5ae"

    characteristic_name_to_uuid = {
        speed: "9c9ec551-771f-4ef5-a3c9-687cd7223370".lower(),        
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
        },
    }

    def read_request(characteristic):
        # str(characteristic) is like: "51ff12bb-3ed8-46e5-b4f9-d64e2fec021b: Unknown"
        characteristic_name = characteristic_uuid_to_name[str(characteristic).split(":")[0].lower()]
        data = obd_data[characteristic_name]
        return bytearray(str(data).encode())

    async def run(loop):
        server = BlessServer(name="obd simulator", loop=loop)
        server.read_request_func = read_request

        await server.add_gatt(gatt)
        await server.start()
    
        while True:
            server.read_request(characteristic_name_to_uuid[speed]) # it does not matter here which characteristic you specify
            await asyncio.sleep(2)


    loop.run_until_complete(run(loop))


loop = asyncio.get_event_loop()

lock = Lock()
simulator_thread = Thread(target=simulate_data, args=(lock,))
gatt_client_thread = Thread(target=gatt_server, args=(lock,loop))

simulator_thread.start()
gatt_client_thread.start()

# end with ctrl+c

