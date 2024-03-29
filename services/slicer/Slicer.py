from config import settings
import sys
import os

COMMAND = '''{number}: L P[{position_index}] {speed} CNT100 COORD PTH  ;'''
skip_start = settings["skip_start"]
skip_end = settings["skip_end"]

SENSOR_POS = (settings["robot_x"] - settings["sensor_x"],
              settings["robot_y"] - settings["sensor_y"],
              settings["sensor_z"])

FIRST_LAYERS_Z = (settings["first_layers"], settings["first_layers_z"])

def fix_path(path):
    path = path.replace('\\', '/')
    if path[-1] != '/':
        path += '/'
    print(path)
    return path


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


try:
    path = []
    use_distance_sensor = False

    path = 'data'
    output_path = 'output_data'

    if len(sys.argv) == 2:
        path = sys.argv[1].replace('\\', '/')
        print(path)
    
    elif len(sys.argv) >= 3:
        path = sys.argv[1]
        output_path = sys.argv[2]
        print(output_path)


    if len(sys.argv) == 4:
        if sys.argv[3] == 'd':
            use_distance_sensor = True
    

    path = fix_path(path)
    output_path = fix_path(output_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)


    head_data = None
    commands_data = []
    position_data = []

    files = sort(os.listdir(path))
    print(files)

    for file in files:
        if file[-3:] != '.ls':
            continue
        with open('{}{}'.format(path, file), 'r') as f:
            strings = f.readlines()
            
        if head_data is None:
            head_start = strings.index('/ATTR\n')
            head_end = strings.index('/MN\n') + 1

            head_data = strings[head_start : head_end]

        commands_start = strings.index('/MN\n') + 1
        commands_end = strings.index('/POS\n') 

        commands_data += strings[commands_start : commands_end]

        position_start = strings.index('/POS\n') + 1
        position_end = strings.index('/END\n')

        position_data += strings[position_start : position_end]

    old_z, z = None, None
    layer_number = 0
    line_number = 1

    collected_data = []
    collected_data.append([])

    collected_data_ds = []
    collected_data_ds.append([])

    hights = []

    position_start = 0

    for data in commands_data:
        data_parts = data.split()   
        if len(data_parts) > 3:
            position_start = position_data.index('{} {{\n'.format(data_parts[2]), position_start) + 1
            position_end = position_data.index('};\n', position_start) + 1
            position_parts = position_data[position_start : position_end]        

            z = position_parts[2].split()[10]
            if old_z is None:
                hights.append(z)
                old_z = z
            if z != old_z:
                hights.append(z)
                layer_number += 1
                line_number = 1
                collected_data.append([])
            old_z = z

            data_parts[0] = '{}:'.format(line_number)
            data_parts[2] = 'P[{}]'.format(line_number)
            if use_distance_sensor:
                position_parts_distance = position_parts.copy()
                coords = position_parts_distance[2].split()
                coords[2] = str(round(float(coords[2]) + SENSOR_POS[0], 2)) ###############################
                coords[6] = str(round(float(coords[6]) + SENSOR_POS[1], 2))  ###############################
                if layer_number < FIRST_LAYERS_Z[0]:
                    coords[10] = str(round(float(coords[10]) + SENSOR_POS[2] + FIRST_LAYERS_Z[1], 2))
                else:
                    coords[10] = str(round(float(coords[10]) + SENSOR_POS[2], 2))
                    
                position_parts_distance[2] = ' '.join(coords)
            
            position_parts = ['P[{}] {{\n'.format(line_number)] + position_parts
            
            if use_distance_sensor:
                position_parts_distance = ['P[{}] {{\n'.format(line_number)] + position_parts_distance
                collected_data[layer_number].append([data_parts,
                                                 position_parts,
                                                     position_parts_distance])
            else:
                collected_data[layer_number].append([data_parts,
                                                 position_parts])

            line_number += 1
                
        else:
            collected_data[layer_number].append(data)
        
    output_folder = output_path.split('/')[-2] if output_path.split('/')[-1] == '' else output_path.split('/')[-1] 
    for layer in range(len(collected_data)):
        name = '{}_{}'.format(output_folder, layer + 1)
        with open('{}{}.ls'.format(output_path, name), 'w') as file:
            file.write('/PROG {}\n'.format(name))
            head_data[4] = 'LINE_COUNT = {};\n'.format(len(collected_data[layer]))
            file.write(''.join(head_data))

            if layer < FIRST_LAYERS_Z[0]:
                file.write(':SR[21]={};\n'.format(float(hights[layer]) + SENSOR_POS[2] + FIRST_LAYERS_Z[1]))
            else:
                file.write(':SR[21]={};\n'.format(float(hights[layer]) + SENSOR_POS[2]))
            file.write(':R[34]=0;\n')

            for data in collected_data[layer]:
                if isinstance(data, list):
                    file.write('{}\n'.format(' '.join(data[0])))
                else:
                    file.write(data)
                    
            
            
            if use_distance_sensor:
                lines_number = len(collected_data[layer])
                for i, data in enumerate(collected_data[layer]):
                    
                    if i == skip_start + 1:
                        file.write(':R[34]=1;\n')
                    elif i == lines_number - skip_end - 1:
                        file.write(':R[34]=0;\n')
                    if isinstance(data, list):
                        #file.write(':SR[23]=$SCR_GRP[1].$MCH_POS_X;\n')
                        #file.write(':SR[24]=$SCR_GRP[1].$MCH_POS_Y;\n')

                        data_parts = data[0].copy()
                        line_number = int(data_parts[0][:-1])
                        data[2][0] = 'P[{}] {{\n'.format(lines_number + line_number)

                        data_parts[0] = '{}:'.format(lines_number + line_number)
                        data_parts[2] = 'P[{}]'.format(lines_number + line_number)
                        if i == 0:
                            data_parts[3] = '{}cm/min'.format(settings["start_speed"])
                        else:
                            data_parts[3] = '{}cm/min'.format(settings["speed"])
                            
                        file.write('{}\n'.format(' '.join(data_parts)))
                        
                 
            file.write('/POS\n')

            for i, data in enumerate(collected_data[layer]):
                if isinstance(data, list):
                    file.write('{}'.format(' '.join(data[1])))
                    if use_distance_sensor:
                        data[2][4] = '      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg\n'
                        file.write('{}'.format(' '.join(data[2])))


            file.write('/END\n')

            
    print('1\nsucces')
    
except Exception as e:
    print('{}\n{}'.format(0, e))

    

