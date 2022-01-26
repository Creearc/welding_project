from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, DINT, STRING

robot = '192.168.0.101'

class Fanuc():
  def __init__(self, ip='192.168.0.101'):
    self.plc = CIPDriver(ip)
    self.ip = ip

  def read_r(self, number):
    with CIPDriver(self.ip) as plc:
      response = plc.generic_message(
              service=b"\x0E", # single
              class_code= b"\x6B",
              instance=1,
              attribute=number,
              connected=False
          )
    if response:
      return 1, response.value
    else:
      return 0, response.error

  def write_r(self, number, data):
    with CIPDriver(self.ip) as plc:
      plc._cfg['cip_path'] = b''
      response = plc.generic_message(
              service=b"\x10", # single
              class_code= b"\x6B",
              instance=1,
              attribute=number,
              request_data=DINT.encode(data),
              connected=False
          )
    if response:
      return 1, response.value
    else:
      return 0, response.error

  def read_sr(self, number):
    with CIPDriver(self.ip) as plc:
      response = plc.generic_message(
              service=b"\x0E", # single
              class_code= b"\x6D",
              instance=1,
              attribute=number,
              connected=False
          )
    if response:
      return 1, response.value
    else:
      return 0, response.error

  def write_sr(self, number, data):
    ss = DINT.encode(len(data)) + '{}{}'.format(
                           #''.join(['\x00' for i in range(3)]),
                           data,
                           ''.join(['\x00' for i in range(84 - len(data))])).encode()
    with CIPDriver(self.ip) as plc:
      plc._cfg['cip_path'] = b''
      response = plc.generic_message(
              service=b"\x10", # single
              class_code= b"\x6D",
              instance=1,
              attribute=number,
              request_data=ss,
              connected=False
          )
    if response:
      return 1, response.value
    else:
      return 0, response.error

if __name__ == '__main__':
  f = Fanuc()
  #print(f.read_r(25))
  #print(f.write_r(25, 8))
  #print(f.read_r(25))
  print(f.read_sr(21))
  print(f.write_sr(12, 'text'))
  print(f.write_sr(22, 'LONG_long_Long_text'))
  print(f.write_sr(10, '     SPACE     SPACE   1   2   3   4   5   6'))
