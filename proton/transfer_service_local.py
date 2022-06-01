import sys
import os
import time
import threading
import zmq
import json
import random

path = sys.path[0].replace('\\', '/')
sys.path.insert(0, '{}/modules'.format(path))

import fake_cip as cip 
import fake_ftp as ftp_functions

FILES_PATH = '/home/pi/files/'

data = dict()
states = dict()
states['state'] = -1
states['z'] = 0
ip = '192.168.0.101'

lock = threading.Lock()
debug = not True


if debug:
  f = cip.Fanuc(ip)
  ftp = ftp_functions.Ftp_connection(ip)
  states['state'] = 0

def process_1():
  global f, ip
  f.r[33][0] = 1
  print('GOGOGOGOGOGOOG')
  while True:
    if f.r[33][0] == 3:
      f.r[33][0] = 2
      print('Layer start')
      time.sleep(2.0)
      print('layer finish')
      f.r[33][0] = 1


def main():
  global data, states, ip, lock
  if debug:
    global f, ftp
    
  is_start = False
  current_file_path = None
  state = 0
  

  file_name = None
  file_to_delete = None
  file_to_delete_time = 0.0
  last_file = None

  layer_finish_time = 0

  old_state = 0


  while True:
    try:
        if states['state'] == -1:
          ftp = ftp_functions.Ftp_connection(ip)
          f = cip.Fanuc(ip)
          print('Connected successfully!')
          
        old_state = state
        state = int(f.read_r(33)[1][0])
        
    
        if state == 1:
          states['state'] = 0
          ''' Robot is ready '''

          if is_start:
            states['state'] = 1
            is_start = False

            file_name, path = current_file_path.split('/')[-1], '/'.join(current_file_path.split('/')[:-1])
            if last_file != None and last_file != file_name:
              file_to_delete = last_file
              file_to_delete_time = time.time()

            f.write_sr(20, file_name[:-3].upper())
            print('Send file status: {}'.format(ftp.send(current_file_path, file_name)))
            last_file = file_name

            f.write_r(33, 3)

        elif state == 0:
          states['state'] = 0
          
        else:
          states['state'] = 1    


        if file_to_delete != None and time.time() - file_to_delete_time > 5.0:
          ftp = ftp_functions.Ftp_connection()
          print('{} was deleted from robot'.format(file_to_delete))
          ftp.delete(file_to_delete)
          file_to_delete = None

        

    except Exception as e:
        print('ERROR -> ', e)
        states['state'] = -1

    with lock:
      tmp = data.copy()
      data = dict()

    if len(tmp.keys()) > 0:
      print('New data received')
      is_start = tmp['is_start']
      current_file_path = tmp['current_file_path']
      ip = tmp['ip']
 
    time.sleep(0.01)

  
  

def server():
  global data, states, lock 

  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.RCVTIMEO = 15000
  socket.bind("tcp://0.0.0.0:5000")

  while True:
    try:
      msg = socket.recv().decode()
      
    except:
      print('No connection to interface')
      time.sleep(0.1)
      continue
    
    print('Message: {}'.format(msg))

    if msg == 'data':
      socket.send_string(json.dumps(data), zmq.NOBLOCK)
      
    elif msg == 'states':
      out = ''
      for element in states.keys():
        out = '{}{}${};'.format(out, element, states[element])
      out = out[:-1]
      print('States:  {}'.format(out))
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
      print('Data:    {}'.format(data))
      socket.send_string('1', zmq.NOBLOCK)



if __name__ == '__main__':
  if debug:
    threading.Thread(target=process_1, args=()).start()
  threading.Thread(target=main, args=()).start()
  threading.Thread(target=server, args=()).start()

  
