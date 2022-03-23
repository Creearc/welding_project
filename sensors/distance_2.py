from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.1.103', 502)
client.connect()

data = client.read_holding_registers(0, 32, unit=1)
k = data.registers[5] / data.registers[31]

while True:
  data = client.read_holding_registers(6, 7, unit=1)
  #print(data.registers)
  print(data.registers[0] * k)
client.close()
