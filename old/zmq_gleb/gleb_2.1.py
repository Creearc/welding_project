import sys
import os
import time
import threading
import zmq
import json


import cip2 as cip
import ftp_functions
import log_functions


data = dict()
states = dict()


class zmq_connection():
  def __init__(self, ip="tcp://127.0.0.1:5000"):
    context = zmq.Context()
    self.socket = context.socket(zmq.REQ)
    self.socket.bind("tcp://127.0.0.1:5000")

  def get_data(self, msg):
    self.socket.send(msg)
    return json.loads(socket.recv())


def get_z(filename):
  f = open(filename, 'r')
  for line in f:
    if line[:-1] == '/POS':
      flag = True
    if flag:
      if line[:-1] == '};':
        coords = s.split('\n')[4].split()
        x, y, z = float(coords[2]), float(coords[6]), float(coords[10])
        break
  f.close()
  return z


def process():
  global data, states
  is_start = False
  stop_after_layer = False
  is_continuous = False
  current_file_path = None
  next_file_path = None
  is_last_file = False
  z = 0
  
  f = cip.Fanuc()
  
  log = log_functions.Log()
  ftp = ftp_functions.Ftp_connection()
  ftp.send('main.tp', '', 'main.tp')
  
  file_name = None
  file_to_delete = None
  file_to_delete_time = 0.0
  
  old_is_continuous = is_continuous
  
  log.add('')
  log.add('___________________________')
  log.add('Программа включена')

  states['state'] = 0

  while True:

    #______________________________________________
    if len(data.keys()) > 0:
      is_start = data['is_start']
      stop_after_layer = data['stop_after_layer']
      is_continuous = data['is_continuous']
      current_file_path = data['current_file_path']
      next_file_path = data['next_file_path']
      is_last_file = data['is_last_file']
    else:
      print(0)
      continue
    
    #______________________________________________
    states['z'] = 0

    state = int(f.read_r(33)[1][0])
    if state == 1:
      states['state'] = 2
      ''' Robot is ready '''
      if file_name != None:
        log.add('{} завершен'.format(file_name))
        
      if is_start:
        if stop_after_layer:
          is_start = False

        file_name = current_file_path
        if last_file != None and last_file != file_name:
          file_to_delete = last_file
          file_to_delete_time = time.time()
          
        f.write_sr(20, file_name[:-3].upper())
        ftp.send(file_name, path+'/', file_name)
        last_file = file_name

        f.write_r(33, 3)
        log.add('{} начат'.format(file_name))

        tmp = file_name.split('_')
        if len(tmp) >= 2:
          z  = tmp[-2]
        else:
          z = -1
      
        if is_last_file:
          is_start = False
          if int(f.read_r(32)[1][0]) == 0:
            f.write_r(33, 99)
          else:
            f.write_r(33, 98)
            
    elif state == 0:
      ''' Program is done '''
      states['state'] = 0
      if file_name != None: log.add('{} завершен'.format(file_name))
    else:
      if is_start:
        states['state'] = 1
        ''' Robot is working '''       
      else:
        states['state'] = 1
        ''' Robot is working [finishing] '''

    weld_state = int(f.read_r(32)[1][0])
    if is_continuous:
      if stop_after_layer:
        if weld_state == 0 or weld_state == 5 or weld_state == 7:
          f.write_r(32, 2)
      else:
        f.write_r(32, 5)
    else:
      f.write_r(32, 6)

    if file_to_delete != None and time.time() - file_to_delete_time > 5.0:
      print('File to delete {}'.format(file_to_delete))
      ftp.delete(file_to_delete)
      file_to_delete = None
            
    time.sleep(0.05)
    

def server():
  global data, states
  
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://127.0.0.1:5000")
   
  while True:
    msg = socket.recv().decode()
    print(msg)
      
    if msg == 'data':
      socket.send_string(json.dumps(data))
    elif msg == 'states':
      out = ''
      for element in states.keys():
        out = '{}{}${};'.format(element, states[element])
      out = out[:-1]
      socket.send_string(out)
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
        data[tmp[0]] = tmp[1]
      print(data)
      socket.send_string('1')



if __name__ == '__main__':
  threading.Thread(target=process, args=()).start()
  threading.Thread(target=server, args=()).start()


