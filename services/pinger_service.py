import os
import subprocess
import time
import threading
import zmq

lock = threading.Lock()
data = dict()
states = dict()
states['state'] = 0

ips = {'robot' : '192.168.0.101',
       'raspberrypi' : '192.168.8.101',}

def main():
    global data, states, lock 
    for name, ip in ips.items():
        #response = os.system("ping -n 1 {}".format(ip))
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        response = subprocess.call('cmd /c "ping -n 1 {}"'.format(ip),
                                   startupinfo=si)
        with lock:
            states[name] = response

    time.sleep(10.0)


def server():
    global data, states, lock 

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.RCVTIMEO = 15000
    socket.bind("tcp://0.0.0.0:5002")

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
