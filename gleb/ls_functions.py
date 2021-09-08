import sys
import os
import time

HEAD = '''/PROG {program_name}
/ATTR
OWNER       = MNEDITOR;
CREATE      = DATE 100-11-20  TIME 09:43:21;
MODIFIED    = DATE 100-12-05  TIME 05:26:29;
LINE_COUNT = {line_count};
PROTECT     = READ_WRITE;
TCD:  STACK_SIZE    = 0,
      TASK_PRIORITY = 50,
      TIME_SLICE    = 0,
      BUSY_LAMP_OFF = 0,
      ABORT_REQUEST = 0,
      PAUSE_REQUEST = 0;
DEFAULT_GROUP   = 1,1,*,*,*;
CONTROL_CODE    = 00000000 00000000;
/MN'''

SPEED = '''{line_number}: L P[{position_index}] 240cm/min CNT100 COORD  ;'''
WELD_SPEED = '''{line_number}: L P[{position_index}] WELD_SPEED CNT100 COORD PTH  ;'''
START = ''': Arc Start[{job}];'''
END = ''': Arc End[{job}];'''

NEXT_PROGRAM = ''': CALL {program_name};'''
POS_START = '''/POS'''
POS_END = '''/END'''
POS = '''P[{position_index}] {{
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = {x} mm, Y = {y} mm, Z = {z} mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
}};'''

settings = {'1' : [1, 2],
            '2 - 5' : [3, 4],
            '6-30 ' : [5, 6]}

def build_settings(settings):
  out = dict()
  for key, value in settings.items():
    if key == '':
      continue
    layers = key.split('-')
    for i in range(int(layers[0]), int(layers[-1]) + 1):
      out[i] = value
  return out


def sort(names):
  """Функция сортировки имен файлов в папке.
     - На вход подаются массив имен файлов.
     - На выходе возвращается отсортированный массив имен файлов."""
  for i in range(len(names) - 1):
    for j in range(len(names) - 1 - i):
      name1, name2 = names[j].split('_'), names[j + 1].split('_')
      if len(name1) == 1:
        continue
      elif len(name2) == 1 and j >= 0:
        names[j], names[j + 1] = names[j + 1], names[j]        
      elif int(name1[1].split('.')[0]) > int(name2[1].split('.')[0]):
        names[j], names[j + 1] = names[j + 1], names[j]
    
  return names


def get_info(filename, commands, positions, layers):
  """Функция извлечения данных о коммандах и кординатах из файла и добавление этих данных к старым даннм.
     - На вход полается имя файла, массив команд и массив координат точек.
     - На выходе возвращаются массив команд и массив координат точек."""
  f = open(filename, 'r')
  flag = False
  s = ''
  for line in f:
    if line[:-1] == '/POS':
      flag = True
    if flag:
      if line[:-1] == '};':
        coords = s.split('\n')[4].split()
        x, y, z = float(coords[2]), float(coords[6]), float(coords[10])
        layers.add(z)
        positions.append([x, y, z])
        s = ''
      s = '{}{}'.format(s, line)
    else:
      command = line.split()
      if len(command) > 2:
        if command[2][0] == 'P':
          commands.append(len(positions) + int(command[2][2 : -1]))
        elif 'Start' in command[2]:
          commands.append('Start')
        elif 'End' in command[2]:
          commands.append('End')

  f.close()
  return commands, positions, layers

def get_data_from_folder(path):
  commands, positions, layers = [], [], set()
  files = os.listdir(path)
  files = sort(files)
  for file in files:
    commands, positions, layers = get_info('{}/{}'.format(path, file), commands, positions, layers)
  layers_count = len(list(layers))
  layers = list(layers)
  layers.sort()
  return commands, positions, layers_count
    
def make_layers(commands, positions, settings):
  """Функция, сохраняющая команды и координаты точек по слоям в виде строк.
     Слой определяется по координате Z.
     - На вход подаются массив команд и массив координат точек.
     - На выходе возвращается массив слоев, каждый элемент которого содержит массив команд
     и массив координат точек в виде строк для записи в ls файл."""
  layers = []
  cs, ps =[], []
  z = None
  line_number = 0
  position_index = 0
  weld_speed = False
  for i in range(len(commands)):
    if commands[i] == 'Start':
      weld_speed = True
      cs.append(START.format(job=1))
      start_ind = len(cs) - 1
      start_point = positions[int(commands[i - 1]) - 1]

    elif commands[i] == 'End':
      weld_speed = False
      if start_ind != None:
        """Проверка наличия замкнутого контура."""
        if start_point == positions[int(commands[i - 1]) - 1]:
          job = settings[len(layers)][1]
        else:
          job = settings[len(layers)][0]
        cs[start_ind] = START.format(job=job)
        cs.append(END.format(job=job))
      
    else:
      line_number += 1
      position_index += 1
        
      index = int(commands[i]) - 1
      if positions[index][2] !=  z or z is None:
        z = positions[index][2]
          
        line_number = 1
        position_index = 1
        layers.append([cs.copy(), ps.copy()])
        cs, ps = [], []
        start_ind = None
      if weld_speed:
        cs.append(WELD_SPEED.format(line_number=line_number,
                                      position_index=position_index))
      else:
        cs.append(SPEED.format(line_number=line_number,
                                      position_index=position_index))

      ps.append(POS.format(position_index=position_index,
                               x=positions[index][0],
                               y=positions[index][1],
                               z=positions[index][2]))
  
  layers.append([cs.copy(), ps.copy()])
  layers.pop(0)
  return layers


def build_ls(otput_folder, i, layer, last):
  otput_file = '{}/{}_{}.ls'.format(otput_folder, otput_folder, i)
  f = open(otput_file, 'w')
  f.write('{}\n'.format(HEAD.format(program_name='{}_{}'.format(otput_folder, i),
                      line_count=len(layer[1]))))
  for command in layer[0]:
    f.write('{}\n'.format(command))
       
  f.write('{}\n'.format(POS_START))
  for point in layer[1]:
    f.write('{}\n'.format(point))
  
  f.write('{}\n'.format(POS_END))
  f.close()


def build_ls_files(otput_folder, commands, positions, settings):
  if not os.path.isdir(otput_folder):
    os.mkdir(otput_folder)
    
  layers = make_layers(commands, positions, settings)
  otput_file = '{}/{}_main.ls'.format(otput_folder, otput_folder)
  f = open(otput_file, 'w')
  f.write('{}\n'.format(HEAD.format(program_name='{}_main'.format(otput_folder),
                      line_count=len(layers))))
  for i, layer in enumerate(layers):
    last = i + 1 == len(layers)
    build_ls(otput_folder, i + 1, layer, last)
    f.write('{}\n'.format(NEXT_PROGRAM.format(program_name='{}_{}'.format(otput_folder, i + 1))))
  f.write('{}\n'.format(POS_START))
  f.write('{}\n'.format(POS_END))
  f.close()
   


def make_ini(path):
  f = open('{}/robot.ini'.format(path), 'w')
  f.write('''[WinOLPC_Util]
Robot=\\C\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1
Version=V7.70-1
Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin
Support=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\support
Output=C:\\Users\\user\\Documents\\My Workcells\\WeldPRO1\\Robot_1\\output''')
  f.close()

def convert_ls_to_tp(path):
  make_ini(path)
  files = os.listdir(path)
  for file in files:
    if file.split('.')[-1] == 'ls':
      os.system('cmd /c "cd {} & maketp {}"'.format(path, file))
