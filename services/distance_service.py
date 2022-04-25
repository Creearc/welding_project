
from pymodbus.client.sync import ModbusTcpClient
import zmq
import cip
from serial import Serial
import time 

client = ModbusTcpClient('192.168.0.105', 502)
client.connect()

data = client.read_holding_registers(0, 32, unit=1)
k = data.registers[5] / data.registers[31]

arduino = Serial(port = 'COM3', baudrate = 9600, timeout = 2)
open_ = "open" + '\n'
close_ = "close" + '\оn'

f = cip.Fanuc()

activate_sensor = False
old_activate_sensor = False

while True:
    try:
        old_activate_sensor = activate_sensor
        activate_sensor = int(f.read_r(33)[1][0]) == 1

        if old_activate_sensor != activate_sensor:
            arduino.write(open_.encode() if activate_sensor else close_.encode())
            time.sleep(1.0)

        if activate_sensor:
            data = client.read_holding_registers(6, 7, unit=1)
            msg = str(data.registers[0] * k)
            print(msg)
            #socket.send(msg.encode('utf-8'))
            

    except Exception as e:
        print(e)
    
