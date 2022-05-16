import sys
import os
import threading
import zmq

lock = threading.Lock()
data = dict()
states = dict()
states['state'] = 0


def make_ini(path):
    f = open('{}/robot.ini'.format(path), 'w')
    f.write('''[WinOLPC_Util]
    Robot=\\C\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1
    Version=V7.70-1
    Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin
    Support=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\support
    Output=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\output''')
    f.close()


def convert_ls_to_tp(path, output_folder):
    make_ini(path)
    files = os.listdir(path)
    for file in files:
        if file.split('.')[-1] == 'ls':
            os.system('cmd /c "cd {} & maketp {}"'.format(path, file))

            filename_path = '{}/{}'.format(path, file.replace('.ls', '.tp'))
            output_file_path = '{}/{}'.format(output_folder, file.replace('.ls', '.tp'))
            os.replace(filename_path, output_file_path)


try:
  path = []
  if len(sys.argv) > 1:
    path = sys.argv[1].replace('\\', '/')
  else:
    path ='out_test_2'

  if os.path.isdir(path):
    if len(sys.argv) > 2:
      output_folder = sys.argv[2].replace('\\', '/')
    else:
      output_folder = path.split('/')
      first = '/'.join(output_folder[:-1])
      last = '{}_TP'.format(output_folder[-1])
      output_folder  = '/'.join([first, last])

    if not os.path.isdir(output_folder):
      os.mkdir(output_folder)

    convert_ls_to_tp(path, output_folder)

  else:
    convert_ls_to_tp_single(path)

  print('1\nsucces')

except Exception as e:
  print('{}\n{}'.format(0, e))

def main():
    global data, states, lock

    path = None

    while True:
        with lock:
            tmp = data.copy()
            data = dict()

        if len(tmp.keys()) > 0:
            print('New data received')
            path = tmp['path']
            if path == 'stop':
                states['state'] = 0
                continue
                
            disk = path[:2]
            path = path[2:]

            states['state'] = 1
            make_ini(path)

            files = []
            for file in os.listdir(path):
                if file.split('.')[-1] == 'ls':
                    files.append(file)
    
            states['max_count'] = len(files)
            count = 0

        if states['state'] == 1:                     
            count += 1
            if count >= len(files):
                states['state'] = 0
                
            states['count'] = count
            os.system('cmd /c "{} & cd {} & maketp {}"'.format(disk, path, files[count - 1]))

        time.sleep(0.01)


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
        print('\033[93m{}\033[0m'.format(msg))

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


      
