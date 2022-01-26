from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT, LINT, ULINT

robot = '192.168.0.101'

class Fanuc():
  def __init__(self, ip='192.168.0.101'):
    self.plc = CIPDriver(ip)

  def read_r(self, number):
    response = self.plc.generic_message(
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
    self.plc._cfg['cip_path'] = b''
    response = self.plc.generic_message(
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


if __name__ == '__main__':
  f = Fanuc()
  print(f.read_r(25))
  print(f.write_r(25, 8))
  print(f.read_r(25))
