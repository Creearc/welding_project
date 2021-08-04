from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT
import time

to_bin = lambda x : bin(int.from_bytes(x, 'big'))[2:]
print(to_bin(b'\n'))

def ask(plc, class_code, instance, attribute):
  response = plc.generic_message(
                    service=b"\x0E", # single
                    class_code= class_code,
                    instance=instance,
                    attribute=attribute,
                    connected=False
                )
  if not response.error:
          print(''' "{} {} {}" : {}  {},'''.format(class_code, instance, attribute,
                                               to_bin(response.value), len(to_bin(response.value))))

with CIPDriver('192.168.0.2') as plc:
  while True:
    ask(plc, b'\xa2', 1, 5)
    ask(plc, b'\xa2', 2, 5)
    time.sleep(0.2)
  
