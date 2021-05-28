import sys
import os
import time

from ftplib import FTP

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
  path ='out_test'

files = os.listdir(path)
out = []
for i in range(len(files)):
  if files[i].split('.')[-1] == 'tp':
    out.append(files[i])

files = out
print(files)

file_count = 18
i = 0
for i in range(file_count):
  print(i, send(ftp, files[i], path))


print('Нажмите ENTER для запуска передачи следующих файлов')
input()
for i in range(file_count, len(files)):
  print(i, send(ftp, files[i], path)) 
  while not is_next(ftp, files[i - file_count]):
    time.sleep(5.0)
