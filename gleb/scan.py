import sys
import os
import time
import threading
import tkinter as tk

import cip2 as cip

def process_2():
  global r, info, s_out, tbox
  info_old = [info[i].get() for i in range(len(info))]
  f = cip.Fanuc()

  while True:
    for i in range(len(r)):
      info[i].set(f.read_r(r[i])[1][0])

    tmp = [info[i].get() for i in range(len(info))]
    if info_old != tmp:
      info_old = tmp.copy()
      s_out.set('{}\n{}'.format(s_out.get(), ' '.join([str(i) for i in info_old])))
      s_out.set('\n'.join(s_out.get().split('\n')[-6:]))

    time.sleep(0.05)
    #f.write_r(33, int(time.time() % 10))
  

r = [i for i in range(31, 34)]
info = []

try:
  master = tk.Tk()
  master.title("Gleb 2.0")

  for i in range(len(r)):
    tk.Label(master, text="R {}".format(r[i]),
           font=("Times New Roman", 12, 'bold'),
             width=10).grid(row=1, column=i)
    info.append(tk.IntVar())
    tk.Entry(master, textvariable=info[-1],
             width=10).grid(row=2, column=i)
  
  s_out = tk.StringVar()
  tk.Label(master, textvariable=s_out,
           font=("Times New Roman", 12),
             width=10, height=10).grid(row=3, column=0,
                            columnspan=len(r))
  
  threading.Thread(target=process_2, args=()).start()
  master.mainloop()
  
except KeyboardInterrupt:
  master.destroy()
  sys.exit()
