import os
import sys
import threading

def make_ini(path):
  f = open('{}/robot.ini'.format(path), 'w')
  f.write('''[WinOLPC_Util]
Robot=\\C\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1
Version=V7.70-1
Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin
Support=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\support
Output=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\output''')
  f.close() 

def convert_ls_to_tp(path, files):
  for file in files:
    os.system('cmd /c "cd {} & maketp {}"'.format(path, file))


path = []
if len(sys.argv) > 1:
  path = sys.argv[1].split('\\')[-1]
else:
  path ='out_test'

files = os.listdir(path)
out = []
for i in range(len(files)):
  if files[i].split('.')[-1] == 'ls':
    out.append(files[i])
    
make_ini(path)
threads_count = 5
part = len(files) // 5
out = []
for j in range(threads_count):
    t = threading.Thread(target=convert_ls_to_tp,
                         args=(path, files[j * part : (j+1) * part],))
    out.append(t)
    t.start()
for t in out:
    t.join()
  
