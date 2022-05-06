import sys
import os
import time
import threading
import tkinter as tk

import cip2 as cip
import ftp_functions
import log_functions

beautiful_float = lambda x : int(x * 100) / 100

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

def convert_ls_to_tp(path):
  make_ini(path)
  files = os.listdir(path)
  for file in files:
    if file.split('.')[-1] == 'ls':
      os.system('cmd /c "cd {} & maketp {}"'.format(path, file))

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

def distance_thread():
  global z_int

  f = cip.Fanuc()

  client = ModbusTcpClient('192.168.0.105', 502)
  client.connect()

  data = client.read_holding_registers(0, 32, unit=1)
  k = data.registers[5] / data.registers[31]

  arduino = Serial(port = 'COM3', baudrate = 9600, timeout = 2)
  open_ = "open" + '\n'
  close_ = "close" + '\n'

  activate_sensor = False
  old_activate_sensor = False

  while True:
    try:
        old_activate_sensor = activate_sensor
        activate_sensor = int(f.read_r(34)[1][0]) == 1

        if old_activate_sensor != activate_sensor:
            arduino.write(open_.encode() if activate_sensor else close_.encode())
            time.sleep(1.0)

            if activate_sensor:
              counter = 0
              summ = 0
              mn, mx = 0, 0

            if not activate_sensor:
              z_int.set('0 (0 0)'.format(beautiful_float(summ / counter),
                                         beautiful_float(mn),
                                         beautiful_float(mx)))
            

        if activate_sensor:
            data = client.read_holding_registers(6, 7, unit=1)
            msg = int(str(data.registers[0] * k).encode('utf-8'))
            print(msg)
            
            if mx < msg:
              mx = msg
            if mn == 0 or mn > msg:
              mn = msg
              
            summ += msg
            counter += 1

          time.sleep(0.01)
            
    except Exception as e:
        print(e)
        

def get_files(path):
  files = os.listdir(path)
  out = []
  for i in range(len(files)):
    if files[i].split('.')[-1] == 'tp' and not('main' in files[i]):
      out.append(files[i])

  files = sort(out)  
  return files

def print_files(files):
  for i in range(len(files)):
    print('{} layer - {}'.format(i+1, files[i]))
  print('________________________________________')

def state_chek():
  f = cip.Fanuc()
  while f.read_r(26)[1] != 1:
    time.sleep(0.1)
  start_button.configure(text="Слой закончен", bg="blue")

def process_2():
  global is_start, files, path, layer_int, z_int, not_auto, last_file
  global is_continuous, timer_int, use_timer, countdown_int
  
  f = cip.Fanuc()
  log = log_functions.Log()
  ftp = ftp_functions.Ftp_connection()
  file_name = None
  file_to_delete = None
  file_to_delete_time = 0.0

  layer_finish_time = 0

  old_state = 0
  
  old_is_continuous = is_continuous.get()
  
  log.add('')
  log.add('___________________________')
  log.add('Программа включена')

  for file in files:
    try:
      ftp.delete(file)
      print('{} was deleted'.format(file))
    except:
      continue
  ftp.close()
  
  while True:
    state = int(f.read_r(33)[1][0])
    if state == 1:
      if layer_finish_time == -1:
        layer_finish_time = time.time()
      if use_timer.get() and layer_finish_time != 0:        
        tmp = timer_int.get() - int(time.time() - layer_finish_time)
        countdown_int.set(tmp)
        if time.time() - layer_finish_time > timer_int.get():
          is_start = True
          layer_int.set(layer_int.get() + 1)
          countdown_int.set(0)
          
      else:
        start_button.configure(text="Запустить", bg="green")
      if file_name != None and old_state != state: log.add('{} завершен'.format(file_name))
      if is_start:
        if not_auto.get():
          is_start = False
          layer_finish_time = -1
        else:
          if last_file != None:
            layer_int.set(layer_int.get() + 1)

        file_name = files[layer_int.get() - 1]
        if last_file != None and last_file != file_name:
          file_to_delete = last_file
          file_to_delete_time = time.time()
          
        f.write_sr(20, file_name[:-3].upper())
        ftp = ftp_functions.Ftp_connection()
        ftp.send(file_name, path+'/', file_name)
        ftp.close()
        last_file = file_name

        f.write_r(33, 3)
        log.add('{} начат'.format(file_name))

        tmp = file_name.split('_')
        if len(tmp) >= 2:
          z_int.set(tmp[-2])
        else:
          z_int.set(-1)
      
        if layer_int.get() > len(files) - 1:
          #layer_int.set(1)
          is_start = False
          if int(f.read_r(32)[1][0]) == 0:
            f.write_r(33, 99)
          else:
            f.write_r(33, 98)    
    elif state == 0:
      start_button.configure(text="Программа завершена", bg="blue")
      if file_name != None and old_state != state: log.add('{} завершен'.format(file_name))
    else:
      if is_start:
        start_button.configure(text="Слой в работе", bg="yellow")       
      else:
        start_button.configure(text="Слой в работе [завершение]", bg="yellow")

    weld_state = int(f.read_r(32)[1][0])
    if is_continuous.get():
      if not_auto.get():
        if weld_state == 0 or weld_state == 5 or weld_state == 7:
          f.write_r(32, 2)
      else:
        f.write_r(32, 5)
    else:
      f.write_r(32, 6)

    if file_to_delete != None and time.time() - file_to_delete_time > 5.0:
      ftp = ftp_functions.Ftp_connection()
      print('File to delete {}'.format(file_to_delete))
      ftp.delete(file_to_delete)
      file_to_delete = None
      ftp.close()

    new_files = get_files(path)
    if new_files != files:
      files = new_files
      print_files(files)

    old_state = state
    time.sleep(0.01)
    

def start_click():
  global is_start, layer_int  
  is_start = not is_start


def nesxt_layer():
  global is_start, layer_int  
  layer_int.set(layer_int.get() + 1)
  is_start = True


def skip_layer():
  global is_start, layer_int 
  layer_int.set(layer_int.get() + 2)
  is_start = True


def repeat_layer():
  global is_start 
  is_start = True


last_file = None
is_start = False
path = []
if len(sys.argv) > 1:
  path = sys.argv[1]
else:
  path ='test_TP'

files = get_files(path)
print_files(files)

ftp = ftp_functions.Ftp_connection()
ftp.send('main.tp', '', 'main.tp')


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
  tk.Label(master, text="Высота:",
           font=("Times New Roman", 44, 'bold')).grid(row=1, column=1, columnspan=3)

  layer_int = tk.IntVar()
  layer_int.set(1)
  tk.Label(master, textvariable=layer_int,
           font=("Times New Roman", 44, 'bold')).grid(row=0, column=4)

  z_int = tk.StringVar()
  z_int.set('0 (0 0)')
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
  
  threading.Thread(target=process_2, args=()).start()
  threading.Thread(target=distance_thread, args=()).start()
  master.mainloop()
  
except KeyboardInterrupt:
  log.add('Программа выключена')
  master.destroy()
  sys.exit()
