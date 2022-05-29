import sys
import os
import threading
import zmq
import time
import subprocess

lock = threading.Lock()
data = dict()
states = dict()
states['state'] = 0

def sort(names):
  """Функция сортировки имен файлов в папке.
     - На вход подаются массив имен файлов.
     - На выходе возвращается отсортированный массив имен файлов."""
  for i in range(len(names) - 1):
    for j in range(len(names) - 1 - i):
      name1, name2 = names[j].split('_'), names[j + 1].split('_')
      #print(name1, name2)
      try:
        if len(name1) == 1:
          continue
        elif len(name2) == 1 and j >= 0:
          names[j], names[j + 1] = names[j + 1], names[j]        
        elif int(name1[-1].split('.')[0]) > int(name2[-1].split('.')[0]):
          names[j], names[j + 1] = names[j + 1], names[j]
      except:
        names[j], names[j + 1] = names[j + 1], names[j]
    
  return names

def make_ini(path):
  f = open('{}/robot.ini'.format(path), 'w')
  f.write('''[WinOLPC_Util]
Robot=\\C\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1
Version=V7.70-1
Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin
Support=C:\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1\\support
Output=C:\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1\\output''')
  f.close()


def main():
    global data, states, lock

    path = None

    while True:
        try:
            with lock:
                tmp = data.copy()
                data = dict()

            if len(tmp.keys()) > 0:
                print('New data received')
                path = tmp['path']
                if path == 'stop':
                    states['state'] = 0
                    continue

                make_ini(path)
                               
                states['state'] = 1
                
                files = []
                for file in os.listdir(path):
                    if file.split('.')[-1] == 'ls':
                        files.append(file)

                files = sort(files)

                disk = path[:2]
                path = path[2:]
        
                states['max_count'] = len(files)
                count = 0

            if states['state'] == 1:                     
                count += 1
                if count >= len(files):
                    states['state'] = 0
                    
                states['count'] = count
                print(files[count - 1])
                #os.system('cmd /c "{} & cd {} & maketp {}"'.format(disk, path, files[count - 1]))
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('cmd /c "{} & cd {} & maketp {}"'.format(disk, path, files[count - 1]),
                                startupinfo=si)
                time.sleep(1.01)

            time.sleep(0.01)
        
        except Exception as e:
            print('{}\n{}'.format(0, e))


def server():
    global data, states, lock 

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.RCVTIMEO = 15000
    socket.bind("tcp://0.0.0.0:5001")

    while True:
        try:
            msg = socket.recv().decode()
        except:
            print('No connection to interface')
            time.sleep(0.1)
            continue
        #print('\033[93m{}\033[0m'.format(msg))

        if msg == 'data':
            socket.send_string(json.dumps(data), zmq.NOBLOCK)
        elif msg == 'states':
            out = ''
            for element in states.keys():
                out = '{}{}${};'.format(out, element, states[element])
            out = out[:-1]
            #print(out)
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


      
