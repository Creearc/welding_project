import zmq
import threading
import json

def server():
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://0.0.0.0:5000")

  data = dict()
  states = {'state' : 1,
            'z' : 0}
   
  while True:
    msg = socket.recv().decode()
    print(msg)
    
    if msg == 'states':
      out = ''
      for element in states.keys():
        out = '{}{}:{};'.format(out, element, states[element])
      out = out[:-1]
      socket.send_string(out)
    else:
      msg = msg.split(';')
      for element in msg:
        tmp = element.split(':')
        if tmp[1] == 'True':
          tmp[1] = True
        elif tmp[1] == 'False':
          tmp[1] = False
        elif tmp[1] == 'None':
          tmp[1] = None
        data[tmp[0]] = tmp[1]
      print(data)
      socket.send_string('1')


threading.Thread(target=server, args=()).start()
