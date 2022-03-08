import sys
import os
import time
import threading
import zmq
import json
import tkinter as tk

import fake_cip as cip
import fake_ftp as ftp_functions

data = dict()
states = dict() # (0Готов  1Печать 2Необходим файл)

lock = threading.Lock()
f = cip.Fanuc()

class zmq_connection():
  def __init__(self, ip="tcp://127.0.0.1:5000"):
    context = zmq.Context()
    self.socket = context.socket(zmq.REQ)
    self.socket.bind("tcp://127.0.0.1:5000")

  def get_data(self, msg):
    self.socket.send(msg, zmq.NOBLOCK)
    return json.loads(socket.recv())

def process_1():
  f.r[33][0] = 1
  while True:
    if f.r[33][0] == 3:
      f.r[33][0] = 2
      print('Layer start')
      time.sleep(2.0)
      print('layer finish')
      f.r[33][0] = 1
      
    

def process_2():
  global data, states, lock, data_var
  is_start = False
  stop_after_layer = False
  is_continuous = False
  current_file_path = None
  next_file_path = None
  is_last_file = False
  last_file = None
  
  ftp = ftp_functions.Ftp_connection()
  file_name = None
  file_to_delete = None
  file_to_delete_time = 0.0

  layer_finish_time = 0

  old_state = 0
  
  while True:
    states['z'] = 0
    
    with lock:
      tmp = data.copy()

    if len(tmp.keys()) > 0:
      print('New data received')
      is_start = tmp['is_start']
      stop_after_layer = tmp['stop_after_layer']
      is_continuous = tmp['is_continuous']
      current_file_path = tmp['current_file_path']
      next_file_path = tmp['next_file_path']
      is_last_file = tmp['is_last_file']

      s = ''.join(['{}: {}\n'.format(key, value) for key, value in tmp.items()])

      data_var.set(s)

      
    state = int(f.read_r(33)[1][0])
    if state == 1:
      states['state'] = 2
      ''' Robot is ready '''
        
      if is_start:
        print('Start IF')
        is_start = False

        file_name, path = current_file_path.split('/')[-1], '/'.join(current_file_path.split('/')[:-1])
        if last_file != None and last_file != file_name:
          file_to_delete = last_file
          file_to_delete_time = time.time()
          
        f.write_sr(20, file_name[:-3].upper())
        ftp.send(file_name, path+'/', file_name)
        last_file = file_name

        f.write_r(33, 3)
      
        if is_last_file:
          is_start = False
          if int(f.read_r(32)[1][0]) == 0:
            f.write_r(33, 99)
          else:
            f.write_r(33, 98)
            
    elif state == 0:
      states['state'] = 0
    else:
      if is_start:
        states['state'] = 1    
      else:
        states['state'] = 1


    if file_to_delete != None and time.time() - file_to_delete_time > 5.0:
      ftp = ftp_functions.Ftp_connection()
      print('File to delete {}'.format(file_to_delete))
      ftp.delete(file_to_delete)
      file_to_delete = None

    old_state = state
    time.sleep(0.01)

def server():
  global data, states, lock 
  
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.RCVTIMEO = 1000
  socket.bind("tcp://127.0.0.1:5000")
   
  while True:
    try:
      msg = socket.recv().decode()
    except:
      print('No connection to interface')
      time.sleep(1.0)
      continue
    print(msg)
      
    if msg == 'data':
      socket.send_string(json.dumps(data), zmq.NOBLOCK)
    elif msg == 'states':
      out = ''
      for element in states.keys():
        out = '{}{}${};'.format(out, element, states[element])
      out = out[:-1]
      socket.send_string(out, zmq.NOBLOCK)
    else:
      msg = msg.split(';')
      for element in msg:
        tmp = element.split('$')
        if tmp[1] == 'True':
          tmp[1] = True
        elif tmp[1] == 'False':
          tmp[1] = False
        elif tmp[1] == 'None':
          tmp[1] = None
        with lock:
          data[tmp[0]] = tmp[1]
      print(data)
      socket.send_string('1', zmq.NOBLOCK)
    with lock:
      data = dict()
      

if __name__ == '__main__':
  master = tk.Tk()
  master.title("Gleb without robot")

  data_var = tk.StringVar()
  data_var.set('No data')
  tk.Label(master, textvariable=data_var,
           font=("Times New Roman", 14, 'bold')).grid(row=1, column=0)

  r_var = tk.StringVar()
  r_var.set(0)
  tk.Label(master, textvariable=r_var,
           font=("Times New Roman", 14)).grid(row=2, column=0)


  threading.Thread(target=process_1, args=()).start()
  threading.Thread(target=process_2, args=()).start()
  threading.Thread(target=server, args=()).start()
  master.mainloop()
