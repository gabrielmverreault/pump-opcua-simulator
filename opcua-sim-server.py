# Adapted from https://github.com/FreeOpcUa/opcua-asyncio/blob/master/examples/server-minimal.py
# Leveraging pump sensor data from Kaggle https://www.kaggle.com/datasets/nphantawee/pump-sensor-data

import asyncio
import logging
import pandas as pd
import re

from asyncua import Server, ua


async def main():
    _logger = logging.getLogger(__name__)
    # Setting up our test server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/pumpsimulator/server/")
    server.set_server_name("Pump Sensor Simulation Server")
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    # Setting up our namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myfolder = await server.nodes.objects.add_folder(idx, "Demo Pump")
    obj_plc1 = await myfolder.add_object(idx, "PLC0001")
    machine_status = await obj_plc1.add_variable(idx, "machine_status", "NORMAL")
    sensors = []
    for i in range(52):
        sensor = await obj_plc1.add_variable(idx, f"sensor_{i:02d}",0.0)
        # set the data type, so we can use it in the client
        sensors.append(sensor) 

    # Read Sensor Data from Kaggle
    df = pd.read_csv("sensor.csv")
    # Select sensor and machine_status columns
    sensor_cols = [col for col in df.columns if re.match('sensor_\d+', col)]
    selected_cols = sensor_cols + ['machine_status']
    sensor_data = df[selected_cols]

    _logger.info("Starting server!")
    async with server:
        # run forever and iterate over the dataframe
        while True:
            for row in sensor_data.itertuples():
                # set sensor values
                for i, sensor in enumerate(sensors):
                    sensor_value = getattr(row, sensor_cols[i])  
                    await sensor.set_value(sensor_value)
                # set machine_status
                machine_status_value = getattr(row, 'machine_status')
                await machine_status.set_value(machine_status_value)
                await asyncio.sleep(0.2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=True)
