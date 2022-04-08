import sys
import os
import time
import threading
import zmq
import json
import random

path = sys.path[0].replace('\\', '/')
sys.path.insert(0, '{}/modules'.format(path))

import cip 
import ftp_functions

FILES_PATH = '/home/pi/files/'

data = dict()
states = dict() # (0Готов  1Печать 2Необходим файл)
states['state'] = 0

lock = threading.Lock()
f = cip.Fanuc()


def main():
  global data, states, lock
  is_start = False
  stop_after_layer = False
  is_continuous = False
  current_file_path = None
  next_file_path = None
  is_last_file = False
  last_file = None

  #ftp = ftp_functions.Ftp_connection()
  file_name = None
  file_to_delete = None
  file_to_delete_time = 0.0

  layer_finish_time = 0

  old_state = 0


  while True:
    states['z'] = random.randint(10, 20) * 0.1

    with lock:
      tmp = data.copy()
      data = dict()

    if len(tmp.keys()) > 0:
      print('New data received')
      is_start = tmp['is_start']
      stop_after_layer = tmp['stop_after_layer'] # to delete
      is_continuous = tmp['is_continuous'] # to delete
      current_file_path = tmp['current_file_path']
      next_file_path = tmp['next_file_path'] # to delete
      is_last_file = tmp['is_last_file'] # to delete

      s = ''.join(['{}: {}\n'.format(key, value) for key, value in tmp.items()])

    try:
        state = int(f.read_r(33)[1][0]) # try except for robot off
    
        if state == 1:
          states['state'] = 0
          ''' Robot is ready '''

          if is_start:
            states['state'] = 1
            print('Start IF')
            is_start = False

            file_name, path = current_file_path.split('/')[-1], '/'.join(current_file_path.split('/')[:-1])
            if last_file != None and last_file != file_name:
              file_to_delete = last_file
              file_to_delete_time = time.time()

            f.write_sr(20, file_name[:-3].upper())
            print('Send file status: {}'.format(ftp.send(file_name, FILES_PATH, file_name)))
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
          states['state'] = 1    


        if file_to_delete != None and time.time() - file_to_delete_time > 5.0:
          ftp = ftp_functions.Ftp_connection()
          print('File to delete {}'.format(file_to_delete))
          ftp.delete(file_to_delete)
          file_to_delete = None

        old_state = state

    except Exception as e:
        print(e)
        states['state'] = -1
 
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
    print(msg)

    if msg == 'data':
      socket.send_string(json.dumps(data), zmq.NOBLOCK)
    elif msg == 'states':
      out = ''
      for element in states.keys():
        out = '{}{}${};'.format(out, element, states[element])
      out = out[:-1]
      print(out)
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



if __name__ == '__main__':
  threading.Thread(target=main, args=()).start()
  threading.Thread(target=server, args=()).start()

  
