import time
import sys


import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://0.0.0.0:5009")


from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.0.105', 502)
client.connect()

data = client.read_holding_registers(0, 32, unit=1)
k = data.registers[5] / data.registers[31]


while True:
  data = client.read_holding_registers(6, 7, unit=1)
  msg = str(data.registers[0] * k)
  socket.send(msg.encode('utf-8'))
  
client.close()
