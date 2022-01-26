import sys
import os

def make_ini(path):
  f = open('{}/robot.ini'.format(path), 'w')
  f.write('''[WinOLPC_Util]
Robot=\\C\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1
Version=V7.70-1
Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin
Support=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\support
Output=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\output''')
  f.close()

PATH = '/'.join(sys.path[0].replace('\\', '/').split('/')[:-1])

paths = []
if len(sys.argv) > 1:
  for i in range(1, len(sys.argv)):
    paths.append(sys.argv[i].split('\\')[-1])
else:
  paths.append('out_test')

for path in paths:
  make_ini(path)
  files = os.listdir(path)
  for file in files:
    print(file)
    if file.split('.')[-1] == 'ls':
      os.system('cmd /c "cd {} & maketp {}"'.format(path, file))
