from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT

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
            service=b"\x0E", # single
            class_code= b"\x6B",
            instance=1,
            attribute=number,
            request_data=INT.encode(data),
            connected=False
        )
    if response:
        return 1, response.value
    else:
        return 0, response.error


with CIPDriver(robot) as plc:
    print(read_register(plc, 25))
    print(write_register(plc, 25, 31))
    print(read_register(plc, 25))
    

