from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT, PADDED_EPATH
import time

to_bin = lambda x : bin(int.from_bytes(x, 'big'))[2:]
reverse = lambda x : x[::-1]
to_normal = lambda x : ''.join([reverse(x[i * 4 : i * 4 + 4]) for i in range(len(x) // 4)])

to_4 = lambda x : [(i, x[i * 4 : i * 4 + 4]) for i in range(len(x) // 4)]
to_8 = lambda x : [(i, x[i * 8 : i * 8 + 8]) for i in range(len(x) // 8)]

two_bytes_value = lambda x, y : int('{}{}'.format(''.join(reverse(x)), ''.join(reverse(y))), base=2)
calc_speed = lambda x : x * 327.67 * 2 / 65535 - 327.67
calc_speed2 = lambda x : x * 327.68 * 2 / 65535
calc_current = lambda x : x * 1000 / 65535
calc_voltage = lambda x : x * 100 / 65535

to_hl = lambda x, y : ''.join([reverse(x[:4]), reverse(x[4:]), reverse(y[:4]), reverse(y[4:])])

def ask(plc, class_code, instance, attribute):
  response = plc.generic_message(
                    service=b"\x0E", # single
                    class_code= class_code,
                    instance=instance,
                    attribute=attribute,
                    connected=False
                )
  if not response.error:
    return response.value


info_template = '''_________________________________________
{code}

Welding start {p0}
Robot ready {p1}
Working modes {p2}
Job number {p3}
Current {p5}
Voltage {p4}
Speed {p6}

Robot to power source
{e1}
{e2}
{e3}
{e4}

Power source to robot
{a1}
{a2}
{a3}
{a4}
{a5}
{a6}
{a7}
{a8}

{s1}
{s2}

{pi}
'''

def info_thread():
  with CIPDriver('192.168.0.2') as plc:
    while True:
      g_info = ask(plc, b'\xa2', 1, 5)
      info = ask(plc, b'\xa2', 2, 5)
      smth1 = ask(plc, b'\xa2', 800, 5)
      smth2 = ask(plc, b'\xa2', 801, 5)
      if info is None:
        continue
      g_info = to_normal(to_bin(g_info))
      info = to_normal(to_bin(info))
      e = to_8(g_info)
      a = to_8(info)
      voltage = calc_voltage(int(to_hl(a[5][1],a[4][1]), base=2))
      current = calc_current(int(to_hl(a[7][1],a[6][1]), base=2))
      speed = calc_speed2(int(to_hl(a[13][1],a[12][1]), base=2))
      if info[24] == '1':
        voltage /= 2
        current /= 2
        speed /= 2
      
      info_text.set(info_template.format(code=0,
                                         p0=g_info[0],
                                         p1=g_info[1],
                                         p2=''.join(g_info[2:5]),
                                         p3=int(''.join(info[16:24]), base=2),
                                         p4=voltage,
                                         p5=current,
                                         p6=speed,

                                         e1=e[:4],
                                         e2=e[4:8],
                                         e3=e[8:12],
                                         e4=e[12:16],
                                         
                                         a1=a[:4],
                                         a2=a[4:8],
                                         a3=a[8:12],
                                         a4=a[12:16],
                                         a5=a[16:20],
                                         a6=a[20:24],
                                         a7=a[24:28],
                                         a8=a[28:32],

                                         s1=smth1,
                                         s2=smth2,
                                       
                                         pi=0))
      time.sleep(0.05)
  
  
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
