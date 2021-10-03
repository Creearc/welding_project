from ftplib import FTP
import sys
import os

class Ftp_connection():
  def __init__(self, ip='192.168.0.101', port=21):
    self.ftp = FTP()
    self.ftp.connect(ip, port)
    self.ftp.login(user='', passwd='')
    
  def send(self, file_path):
    try:
      file = file_path.split('\\')[-1]
      with open(file_path, 'rb') as f:
        self.ftp.storbinary('STOR ' + file, f, 1024)
      return True
    except:
      return False

  def delete(self, file, path):
    self.ftp.delete(path + file)

ftp = Ftp_connection()

path = []
if len(sys.argv) > 1:
  path = sys.argv[1]
else:
  path ='out_test_2'

if os.path.isdir(path):
  for file in os.listdir(path):
    print(file, ftp.send('{}\\{}'.format(path, file)))

else:
  print(path, ftp.send(path))

input('Готово')
