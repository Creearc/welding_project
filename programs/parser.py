import cv2
import numpy as np
import random


def get_info(filename='ls_files/qwerty.ls'):
  f = open(filename, 'r')

  commands = []
  positions = []
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
          commands.append(command[2][2 : -1])
        elif 'Start' in command[2]:
          commands.append('Start')
        elif 'End' in command[2]:
          commands.append('End')
        else:
          commands.append(None)

  f.close()
  return commands, positions

def show(commands, positions):
  out = np.zeros((1024, 1024, 3), np.uint8)
  z = 3
  draw = False
  for i in range(len(commands)):
    if commands[i] == 'Start':
      color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
      draw = True
      start_point = positions[int(commands[i - 1])]
      
    elif commands[i] == 'End':
      draw = False
      print(start_point, positions[int(commands[i - 1]) - 1])
      if start_point == positions[int(commands[i - 1]) - 1]:
        print(1)
      z += 1
      
    elif commands[i] != None:
      if draw:
        index = int(commands[i]) - 1
        print(index)
        if commands[i - 1] == 'Start':
          last_index = index - 1
          #z = int(positions[index - 1][2])
        else:
          last_index = index - 1
        cv2.line(out, (512 + 2 * int(positions[last_index][0]), 512 + 2 * int(positions[last_index][1])),
                  (512 + 2 * int(positions[index][0]), 512 + 2 * int(positions[index][1])), color, 1)
      cv2.imshow('{}'.format(z), out)
      cv2.waitKey(1)
  
#commands, positions = get_info('out_ls_files/3.ls')
commands, positions = get_info()
print(len(commands), len(positions))
show(commands, positions)


