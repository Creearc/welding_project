s = b'\xfd\x00\x00\t\x95*\xe1-J\x00\x00\x00\x8c\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
s2 = b'\xf0\x00\x00\t\x8e)\x161\x00\x00\x00\x00\xa6\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
to_bin = lambda x : bin(int.from_bytes(x, 'big'))[2:]
reverse = lambda x : x[::-1]
to_normal = lambda x : ''.join([reverse(x[i * 4 : i * 4 + 4]) for i in range(len(x) // 4)])

to_4 = lambda x : [x[i * 4 : i * 4 + 4] for i in range(len(x) // 4)]

info = to_normal(to_bin(s))

info_template = '''
Welding start {p0}
Robot ready {p1}
Working modes {p2}
Job number {p3}
Program number {p4}


{pi}
'''

def info_thread():
  i = 0
  from record_1_n import arr
  ln = 0
  for l in arr:
    info = to_normal(to_bin(l))
    #info = to_bin(l[18:-1].encode())
    if i % 2 == 1:

      #print('{} {}'.format(i, l[18:-1]))
      print(to_4(info))
      if ln == 0:
        ln = len(info)
      if ln != len(info):
        break
      info_text.set(info_template.format(p0=info[0],
                                         p1=info[1],
                                         p2=''.join(info[2:5]),
                                         p3=int(''.join(info[16:24]), base=2),
                                         p4=int(''.join(info[24:31]), base=2),
                                         pi=i))
      time.sleep(0.02)
    i += 1


import threading
import time

try:  
  import tkinter as tk
  master = tk.Tk()
  info_text = tk.StringVar()
  tk.Label(master, textvariable=info_text, justify=tk.LEFT).grid(row=1, column=0)

  threading.Thread(target=info_thread, args=()).start()

  master.mainloop()

except KeyboardInterrupt:
  master.destroy()
  sys.exit()
