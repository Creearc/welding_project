import sys
import os
import time
import threading
import tkinter as tk

import cip2 as cip
import ftp_functions

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

def state_chek():
  f = cip.Fanuc()
  while f.read_r(26)[1] != 1:
    time.sleep(0.1)
  start_button.configure(text="Слой закончен", bg="blue")

def process_2():
  global is_start, files, path, layer_int, z_int, not_auto, last_file, is_continuous 
  f = cip.Fanuc()
  ftp = ftp_functions.Ftp_connection()
  
  old_is_continuous = is_continuous.get()

  while True:
    z_int.set(int(f.read_r(30)[1][0]))

    state = int(f.read_r(33)[1][0])
    if state == 1:
      start_button.configure(text="Запустить", bg="green")
      if is_start:
        if not_auto.get():
          is_start = False
        else:
          if last_file != None:
            layer_int.set(layer_int.get() + 1)

        file_name = files[layer_int.get() - 1]
        if last_file != None and last_file != file_name:
          ftp.delete(last_file, path+'/')

        f.write_sr(20, file_name[:-3].upper())
        ftp.send(file_name, path+'/', file_name)
        last_file = file_name

        f.write_r(33, 3)
      
        if layer_int.get() == len(files)+1:
          if int(f.read_r(32)[1][0]) == 0:
            f.write_r(33, 99)
          else:
            f.write_r(33, 98)    
    else:
      if is_start:
        start_button.configure(text="Слой в работе", bg="yellow")       
      else:
        start_button.configure(text="Слой в работе [завершение]", bg="yellow")

    weld_state = int(f.read_r(32)[1][0])
    if is_continuous.get():
      if not_auto.get():
        if weld_state == 0 or weld_state == 5:
          f.write_r(32, 2)
      else:
        f.write_r(32, 5)
    else:
      f.write_r(32, 6)
            
    time.sleep(0.05)
    

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
  path = sys.argv[1].split('\\')[-1]
else:
  path ='t1'

files = os.listdir(path)
out = []
for i in range(len(files)):
  if files[i].split('.')[-1] == 'tp' and not('main' in files[i]):
    out.append(files[i])

files = sort(out)
for i in range(len(files)):
  print('{} layer - {}'.format(i+1, files[i]))
print('________________________________________')

ftp = ftp_functions.Ftp_connection()
ftp.send('main.tp', '', 'main.tp')

try:
  master = tk.Tk()
  master.title("Gleb 2.0")
  
  start_button = tk.Button(master, text="Старт", bg="white",
            width=20, height=3, command=start_click)
  start_button.grid(row=0, column=0)

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
  master.mainloop()
  
except KeyboardInterrupt:
  master.destroy()
  sys.exit()
