import sys
import os
import time
import threading
import tkinter as tk
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")
lock = threading.Lock()

files = ['W:/path/to/file/test_{}.tp'.format(i) for i in range(10)]

data = {'current_file_path' : files[0],
          'is_start' : False,
          'stop_after_layer' : False,
          'is_continuous' : False, 
          'next_file_path' : None,
          'is_last_file' : False}

def send(data):
  out = ''
  for element in data.keys():
    out = '{}{}${};'.format(out, element, data[element])
  out = out[:-1]
  with lock:
    socket.send_string(out, zmq.NOBLOCK)
    print(socket.recv())

def get(msg):
  with lock:
    socket.send_string(msg, zmq.NOBLOCK)
    msg = socket.recv().decode()  
  msg = msg.split(';')
  out = dict()
  for element in msg:
    tmp = element.split('$')
    if tmp[1] == 'True':
      tmp[1] = True
    elif tmp[1] == 'False':
      tmp[1] = False
    elif tmp[1] == 'None':
      tmp[1] = None
    out[tmp[0]] = tmp[1]      
  return out
  

def process_1():

  while True:
    out = get('states')
    print(out)
    time.sleep(0.1)
    

def start_click():
  global layer_int  
  data['is_start'] = True
  send(data)
  data['is_start'] = False

def nesxt_layer():
  global layer_int  
  data['is_start'] = True
  data['current_file_path'] = files[layer_int.get() + 1]
  send(data)
  data['is_start'] = False

def skip_layer():
  global layer_int  
  data['is_start'] = True
  data['current_file_path'] = files[layer_int.get() + 2]
  send(data)
  data['is_start'] = False

def repeat_layer():
  global layer_int  
  data['is_start'] = True
  send(data)
  data['is_start'] = False

try:
  master = tk.Tk()
  master.title("Gleb 2.5")
  
  start_button = tk.Button(master, text="Старт", bg="white",
            width=20, height=3, command=start_click)
  start_button.grid(row=0, column=0)

  countdown_int = tk.IntVar()
  countdown_int.set(0)
  tk.Label(master, textvariable=countdown_int,
           font=("Times New Roman", 44, 'bold')).grid(row=1, column=0)

  tk.Label(master, text="Текущий слой:",
           font=("Times New Roman", 44, 'bold')).grid(row=0, column=1, columnspan=3)
  tk.Label(master, text="Текущая высота:",
           font=("Times New Roman", 44, 'bold')).grid(row=1, column=1, columnspan=3)

  layer_int = tk.IntVar()
  layer_int.set(1)
  tk.Label(master, textvariable=layer_int,
           font=("Times New Roman", 44, 'bold')).grid(row=0, column=4)

  z_int = tk.IntVar()
  z_int.set(0)
  tk.Label(master, textvariable=z_int,
           font=("Times New Roman", 44, 'bold')).grid(row=1, column=4)

  not_auto = tk.BooleanVar()
  tk.Checkbutton(master, text="Остановка после слоя",
                 variable=not_auto,
                 onvalue=1, offvalue=0,
                 width=20, height=3).grid(row=3, column=0)

  use_timer = tk.BooleanVar()
  tk.Checkbutton(master, text="Использовать таймер (секунды)",
                 variable=use_timer,
                 onvalue=1, offvalue=0,
                 width=25, height=3).grid(row=3, column=1)
  timer_int = tk.IntVar()
  timer_int.set(10)
  tk.Entry(master, textvariable=timer_int).grid(row=3, column=2)

  is_continuous = tk.BooleanVar()
  tk.Checkbutton(master, text="Непрерывная наплавка",
                 variable=is_continuous,
                 onvalue=1, offvalue=0,
                 width=20, height=3).grid(row=4, column=0)

  tk.Button(master, text="[+1] Следующий слой", bg="white",
            width=20, height=3, command=nesxt_layer).grid(row=5, column=0)

  tk.Button(master, text="[+2] Пропустить слой", bg="white",
            width=20, height=3, command=skip_layer).grid(row=6, column=0)

  tk.Button(master, text="[0] Повторить слой", bg="white",
            width=20, height=3, command=repeat_layer).grid(row=7, column=0)

  tk.Label(text="Задать слой вручную:").grid(row=8, column=0)
  tk.Entry(master, textvariable=layer_int).grid(row=9, column=0)

  threading.Thread(target=process_1, args=()).start()
  master.mainloop()
  
except KeyboardInterrupt:
  master.destroy()
  sys.exit()
