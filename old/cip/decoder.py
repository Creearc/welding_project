s = b'\xfd\x00\x00\t\x95*\xe1-J\x00\x00\x00\x8c\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
s2 = b'\xf0\x00\x00\t\x8e)\x161\x00\x00\x00\x00\xa6\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
to_bin = lambda x : bin(int.from_bytes(x, 'big'))[2:]
reverse = lambda x : x[::-1]
to_normal = lambda x : ''.join([reverse(x[i * 4 : i * 4 + 4]) for i in range(len(x) // 4)])

to_4 = lambda x : [x[i * 4 : i * 4 + 4] for i in range(len(x) // 4)]

two_bytes_value = lambda x, y : int('{}{}'.format(''.join(x), ''.join(y)), base=2)
calc_speed = lambda x : x * 327.67 * 2 / 65535 - 327.67

#print(calc_speed(0), calc_speed(65535), calc_speed(65535 // 2), calc_speed(65535 // 4 * 3))

info_template = '''_________________________________________
{code}

Welding start {p0}
Robot ready {p1}
Working modes {p2}
Job number {p3}
Main current set value {p4}
Wire speed {p5}
Wire speed 2 {p6}
Wire speed 3 {p7}

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
      """print(to_4(info))
      if ln == 0:
        ln = len(info)
      if ln != len(info):
        break"""
      info_text.set(info_template.format(code=0,
                                         p0=info[0],
                                         p1=info[1],
                                         p2=''.join(info[2:5]),
                                         p3=int(''.join(info[16:24]), base=2),
                                         p4=two_bytes_value(info[40:48], info[32:40]),
                                         p5=calc_speed(two_bytes_value(info[104:112],
                                                                       info[96:104])),
                                         p6=calc_speed(two_bytes_value(info[56:64],
                                                                       info[48:56])),
                                         p7=calc_speed(two_bytes_value(info[40:48],
                                                                       info[32:40])),
                                         pi=i))
      time.sleep(0.02)
      print(calc_speed(int(''.join(info[96:112]), base=2)),
            calc_speed(int(''.join(info[48:64]), base=2)))
    else:
      print(calc_speed(two_bytes_value(info[104:112], info[96:104])),
            calc_speed(two_bytes_value(info[224:232], info[216:224])))
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
