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

def convert_ls_to_tp(path, otput_folder):
  make_ini(path)
  files = os.listdir(path)
  for file in files:
    if file.split('.')[-1] == 'ls':
      os.system('cmd /c "cd {} & maketp {}"'.format(path, file))

      filename_path = '{}/{}'.format(path, file.replace('.ls', '.tp'))
      output_file_path = '{}/{}'.format(otput_folder, file.replace('.ls', '.tp'))
      os.replace(filename_path, output_file_path)

def convert_ls_to_tp_single(way):
  file = way.split('.')[-1]
  path = '/'.join(way.split('/')[:-1])
  make_ini(path)
  if file.split('.')[-1] == 'ls':
    os.system('cmd /c "cd {} & maketp {}"'.format(path, way))

try:
  path = []
  if len(sys.argv) > 1:
    path = sys.argv[1].replace('\\', '/')
  else:
    path ='out_test_2'

  if os.path.isdir(path):
    otput_folder = path.split('/')
    first = '/'.join(otput_folder[:-1])
    last = '{}_TP'.format(otput_folder[-1])
    otput_folder  = '/'.join([first, last])

    if not os.path.isdir(otput_folder):
      os.mkdir(otput_folder)

    convert_ls_to_tp(path, otput_folder)

  else:
    convert_ls_to_tp_single(path)

  print('1\nsucces')

except Exception as e:
  print('{}\n{}'.format(0, e))

