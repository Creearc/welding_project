import zmq
import threading
import time

lock = threading.Lock()
msg = None

def ask(socket, msg):
  socket.send(msg)
  out = socket.recv()
  return out


def answer():
  pass


def listener():
  global lock, msg
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://0.0.0.0:5000")

  while True:
    with lock:
      msg = socket.recv()
    print("Got", msg)


def sender():
  global lock, msg
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://0.0.0.0:5000")

  while True:
    #msg = time.ctime().encode()
    msg = socket.recv()
    with lock:
      print('server', msg)
    socket.send(msg)
    print(1)


def client():
  global lock
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://127.0.0.1:5000")
   
  for i in range(10):
      msg = time.ctime().encode()
      socket.send(msg)
      with lock:
        print("Sending", msg)
      msg_in = socket.recv()

      
#threading.Thread(target=listener, args=()).start()
threading.Thread(target=sender, args=()).start()
for i in range(10):
  threading.Thread(target=client, args=()).start()
