#pip install modbus_tk

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp


slaveIP = '192.168.1.103' # default - 192.168.1.103
slavePort = 502 # default - 502

master = modbus_tcp.TcpMaster(host=slaveIP, port=int(slavePort))
#master = modbus_rtu.RtuMaster(serial.Serial(“COM1”, baudrate=9600))
master.set_timeout(1.0)

'''
с адреса регистра 0, получаем 10 регистров дискретных сигналов (ТС)

getDI=master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 10)


master.execute(1,сst.READ_COILS, 0, 10) 
master.execute(1,cst.READ_INPUT_REGISTERS, 100, 3) 
master.execute(1,cst.READ_HOLDING_REGISTERS, 100, 12)
'''

#data = master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 40100)
data = master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 10)
print(data)


















