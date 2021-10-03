from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT

convert = lambda x : SINT.encode(x)

with CIPDriver('192.168.0.101') as plc:
  for i in range(4, 512):
    print(i, convert(i))

    error_k = 0
    for k in range(100, 5000):
      error = 0
      for j in range(3, 5000):
        response = plc.generic_message(
                    service=b"\x0E", # single
                    class_code=convert(i),
                    instance=k,
                    attribute=j,
                    connected=False
                )
        if not response.error:
          error = 0
          error_k = 0
          print('''{} "{} {} {}" : {},'''.format(i, convert(i), k, j, response.value))
        else:
          #print(response.error)
          error += 1
          if error > 2:
            error_k += 1
            break
                    
      if error_k > 200:
        break
