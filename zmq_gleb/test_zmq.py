import zmq
import threading
import json


def server():
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://127.0.0.1:5000")
   
  while True:
      msg = socket.recv()
      print("Got", msg)
      socket.send(msg)


def client():
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://127.0.0.1:5000")
   
  for i in range(10):
      msg = 'text {}'.format(i).encode()
      socket.send(msg)
      print("Sending", msg)
      msg_in = socket.recv()


def client2():
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://127.0.0.1:5000")

  data = {'current_file_path' : '1.txt',
          'is_start' : False,
          'stop_after_layer' : False,
          'is_continuous' : False, 
          'next_file_path' : None,
          'is_last_file' : False}
   
  

  msg = json.dumps(data)
  socket.send_string(msg)
  print(socket.recv())
  
  msg = 'data'
  socket.send_string(msg)
  data = json.loads(socket.recv())
  print(data['filename'])


threading.Thread(target=client2, args=()).start()
#threading.Thread(target=server, args=()).start()
