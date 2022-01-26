from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT, LINT, ULINT

robot = '192.168.0.101'

def read_register(plc, number):
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

def write_register(plc, number, data):
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

def ask(plc, class_code, instance, attribute, service=b"\x0E", data=None):
  response = plc.generic_message(
                    service=service, 
                    class_code= class_code,
                    instance=instance,
                    attribute=attribute,
                    request_data=data if data is not None else b'',
                    connected=False
                )
  if not response.error:
    return response.value
  else:
    return response.error

with CIPDriver(robot) as plc:
    print(read_register(plc, 25))
    print(write_register(plc, 25, 31))
    print(read_register(plc, 25))

    print(read_register(plc, 29))

    print(ask(plc,
              class_code=b'\x04',
              instance=103,
              attribute=3,
              service=b"\x0E"))

'''    
s = b'\x0b\x01\x01\x00\x99\x99\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
s = b'\n\x00\x01\x00\x99\x99\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
with CIPDriver('192.168.0.2') as plc:
    print(ask(plc, b'\xa2', 1, 5, b"\x0E"))
    #print(DINT.encode(45))
    print(ask(plc, b'\xa2', 1, 5, b"\x10", s))
'''
