# pump-opcua-simulator
Basic OPC UA Server with real historical data from pump sensors streaming as real-time data

## Pre-reqs

- Python 3.8+
  - `pip install python`
- Install opcua-asyncio
  - From: <https://github.com/FreeOpcUa/opcua-asyncio>
  - `pip install asyncua`
- Download the sample data set from Kaggle
  - <https://www.kaggle.com/datasets/nphantawee/pump-sensor-data>
- Extract the data set and store it in the working directory as `sensor.csv`
- Run the OPC UA Server `python opcua-sim-server.py`
