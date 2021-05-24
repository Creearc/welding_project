import sys
import os

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

def sort(names):
  for i in range(len(names) - 1):
    for j in range(len(names) - 1 - i):
      name1, name2 = names[j].split('_'), names[j + 1].split('_')
      if len(name1) == 1:
        continue
      elif len(name2) == 1 and j > 0:
        names[j], names[j + 1] = names[j + 1], names[j]        
      elif int(name1[1].split('.')[0]) > int(name2[1].split('.')[0]):
        names[j], names[j + 1] = names[j + 1], names[j]
    
  return names

def is_near(pos1, pos2):
  x1, y1, z1 = pos1
  x2, y2, z2 = pos2
  if abs(x1 - x2) < 6.0 and abs(y1 - y2) < 6.0 and abs(z1 - z2) < 6.0:
    return True
  else:
    return False

def get_info(filename, commands, positions):
  f = open(filename, 'r')
  flag = False

  for line in f:
    if line[:-1] == '/POS':
      flag = True
      s = ''
    elif line[:-1] == '};':
      coords = s.split('\n')[4].split()
      x, y, z = float(coords[2]), float(coords[6]), float(coords[10])
      positions.append([x, y, z])
      s = ''
    if flag:
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
        else:
          commands.append(None)

  f.close()
  return commands, positions


def make_layers(commands, positions):
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
      #print(len(layers), start_ind, len(cs))
      if start_ind != None:
        #print(start_point, positions[int(commands[i - 2])])
        if start_point == positions[int(commands[i - 1]) - 1]:# or is_near(start_point, positions[int(commands[i - 2])]):
          print(len(layers) - 1, len(ps), start_point, positions[int(commands[i - 1])])
          cs[start_ind] = START.format(job=2)
          cs.append(END.format(job=2))
        else:
          cs[start_ind] = START.format(job=1)
          cs.append(END.format(job=1))
      else:
        print(len(layers) - 1)
      

    elif commands[i] != None:
      if isinstance(commands[i], int):
        line_number += 1
        position_index += 1
        
        index = int(commands[i]) - 1
        if (int(positions[index][2]) !=  z) or (z is None):
          z = int(positions[index][2])
          
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
  layers.pop(0)
  return layers


def build_ls(otput_folder, i, layer, last):
  otput_file = '{}/p{}.ls'.format(otput_folder, i)
  f = open(otput_file, 'w')
  f.write('{}\n'.format(HEAD.format(program_name='p{}'.format(i),
                      line_count=len(layer[1]))))
  for command in layer[0]:
    f.write('{}\n'.format(command))
    
  if not last:
    f.write('{}\n'.format(NEXT_PROGRAM.format(program_name='p{}'.format(i+1))))
    
  f.write('{}\n'.format(POS_START))
  for point in layer[1]:
    f.write('{}\n'.format(point))
  
  f.write('{}\n'.format(POS_END))
  f.close()


paths = []
if len(sys.argv) > 1:
  for i in range(1, len(sys.argv)):
    paths.append(sys.argv[i].split('\\')[-1])
else:
  paths.append('ls_files')

for path in paths:
  otput_folder = 'out_{}'.format(path)
  if not os.path.isdir(otput_folder):
    os.mkdir(otput_folder)

  commands, positions = [], []
  files = os.listdir(path)
  files = sort(files)
  for file in files:
    print(file)
    commands, positions = get_info('{}/{}'.format(path, file), commands, positions)

  layers = make_layers(commands, positions)
  for i, layer in enumerate(layers):
    last = i + 1 == len(layers)
    build_ls(otput_folder, i, layer, last)


    
