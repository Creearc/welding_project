from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT

with CIPDriver('192.168.0.2') as plc:
  for i in range(1, 512):
    error_k = 0
    for k in range(1, 5000):
      error = 0
      for j in range(0, 5000):
        response = plc.generic_message(
                    service=b"\x0E", # single
                    class_code=INT.encode(i),
                    instance=k,
                    attribute=j,
                    connected=False
                )
        if not response.error:
          error = 0
          error_k = 0
          print(''' "{} {} {}" : {},'''.format(INT.encode(i), k, j, response.value))
        else:
          #print(response.error)
          error += 1
          if error > 5:
            error_k += 1
            break
                    
      if error_k > 100:
        break
