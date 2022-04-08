import sys
import os
import time
import threading
import tkinter as tk

path = sys.path[0].replace('\\', '/')
sys.path.insert(0, '{}/modules'.format(path))

import ftp_functions

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
  
  threading.Thread(target=process_2, args=()).start()
  master.mainloop()
  
except KeyboardInterrupt:
  log.add('Программа выключена')
  master.destroy()
  sys.exit()
