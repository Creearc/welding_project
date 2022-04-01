import os

COMMAND = '''{number}: L P[{position_index}] {speed} CNT100 COORD PTH  ;'''

def fix_path(path):
    if path[-1] != '/':
        path += '/'
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

path = fix_path('data2')
output_path = fix_path('output_data')

if not os.path.exists(output_path):
    os.makedirs(output_path)


commands_data = []

files = sort(os.listdir(path))

for file in files:
    with open('{}{}'.format(path, file), 'r') as f:
        strings = f.readlines()

    commands_start = strings.index('/MN\n') + 1
    commands_end = strings.index('/POS\n') - 1

    commands_data += strings[commands_start : commands_end]

print(commands_data[:10])












































































































