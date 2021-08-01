# -*- coding: cp1251 -*-
from ftplib import FTP
import sys


files = []
if len(sys.argv) > 1:
  for i in range(1, len(sys.argv)):
    print(sys.argv[i])
    files.append(sys.argv[i])
else:
  files.append('awsched.va')



ftp = FTP()
HOST = '192.168.0.101'
PORT = 21

ftp.connect(HOST, PORT)
print(ftp.login(user='', passwd=''))

for file in files:
  with open(file, 'rb') as f:
    ftp.storbinary('STOR ' + file, f, 1024)

