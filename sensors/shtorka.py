from serial import Serial
from time import sleep

#arduino = Serial(port = '/dev/ttyUSB0', baudrate = 9600, timeout = 2)
arduino = Serial(port = 'COM3', baudrate = 9600, timeout = 2)
open_ = "open" + '\n'
close_ = "close" + '\оn'

for i in range(100):
    arduino.write(open_.encode())
    sleep(2)
    arduino.write(close_.encode())
    sleep(2)
    print(i)
