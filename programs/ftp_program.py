import sys
import os
import time

from ftplib import FTP

def sort(names):
  """Функция сортировки имен файлов в папке.
     - На вход подаются массив имен файлов.
     - На выходе возвращается отсортированный массив имен файлов."""
  for i in range(len(names) - 1):
    for j in range(len(names) - 1 - i):
      name1, name2 = names[j].split('_'), names[j + 1].split('_')
      #print(name1, name2)
      try:
        if len(name1) == 1:
          continue
        elif len(name2) == 1 and j >= 0:
          names[j], names[j + 1] = names[j + 1], names[j]        
        elif int(name1[-1].split('.')[0]) > int(name2[-1].split('.')[0]):
          names[j], names[j + 1] = names[j + 1], names[j]
      except:
        names[j], names[j + 1] = names[j + 1], names[j]
    
  return names

def send(ftp, file, path):
  try:
    with open('{}/{}'.format(path, file), 'rb') as f:
      ftp.storbinary('STOR ' + file, f, 1024)
    return True
  except:
    return False


def is_next(ftp, file):
  try:
    ftp.delete(file)
    return True
    
  except:
    return False


HOST = '192.168.0.101'
PORT = 21

ftp = FTP()
ftp.connect(HOST, PORT)
ftp.login(user='', passwd='')

path = []
if len(sys.argv) > 1:
  path = sys.argv[1].split('\\')[-1]
else:
  path ='otlivka_ls'

files = os.listdir(path)
out = []
for i in range(len(files)):
  if files[i].split('.')[-1] == 'tp':
    out.append(files[i])

files = sort(out)
print(files)

file_count = 2
i = 0
for i in range(file_count):
  print(i, send(ftp, files[i], path), files[i])


print('Нажмите ENTER для запуска передачи следующих файлов')
input()
for i in range(file_count, len(files)):
  print(i, send(ftp, files[i], path), files[i]) 
  while not is_next(ftp, files[i - file_count + 1]):
    time.sleep(5.0)

#$AWESCH[1,1].$CMD_AMPS
