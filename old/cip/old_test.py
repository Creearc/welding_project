def get_info():
    with CIPDriver(robot) as plc:
        response = plc.generic_message(
            service=b"\x0E", # single
            #service=b"\x10", # all
            class_code= b"\x6B",
            instance=1,
            attribute=18,
            data_type=USINT,
            #request_data=b'\x05\x00\x00\x00',
            #unconnected_send=True,
            #route_path=True,
            connected=False
        )

        if response:
            print(response.value)
            #return ':'.join(f'{x:0>2x}' for x in response.value)
        else:
            print(f'error:    {response.error}')

def put_info():
    with CIPDriver(robot) as plc:
        #plc._sequence = 0
        plc._cfg['cip_path'] = b''
        response = plc.generic_message(
            #service=b"\x0E", # single
            service=b"\x10", # all
            class_code= b"\x6B",
            instance=1,
            attribute=18,
            name=None,
            #data_type=DINT,
            request_data=INT.encode(32000),
            #unconnected_send=True,
            #route_path=True,
            connected=False
        )
        print(response)
        if response:            
            return ':'.join(f'{x:0>2x}' for x in response.value)
        else:
            print(f'error:    {response.error}')

def get_digit():
    with CIPDriver(robot) as plc:
        response = plc.generic_message(
            #service=b"\x0E", # single
            service=b"\x0E", # all
            class_code= b"\x04",
            instance=b"\x321",
            attribute=b"\x03",
            data_type=DINT,
            #request_data=UDINT.encode(5),
            #unconnected_send=True,
            #route_path=True,
            connected=False
        )

        if response:
            print(response)
            return ':'.join(f'{x:0>2x}' for x in response.value)
        else:
            print(f'error:    {response.error}')
