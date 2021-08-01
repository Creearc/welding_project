import sys
import socket
import threading
import time

lock = threading.Lock()

def from_robot(server, client):
  while True:
    data, address = s.recvfrom(4096)
    server.sendto(data, IP2)
    print('____________\nfrom Robot {}\n'.format(data))

def from_fronius(server, client):
  while True:
    data, address = client.recvfrom(4096)
    client.sendto(data, IP1)
    print('____________\nfrom Fronius {}\n'.format(data))

    


PORT = 44818
IP1 = '192.168.0.101'
IP2 = '192.168.0.2'

sock_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

#sock_1.settimeout(15.0)
#sock_2.settimeout(15.0)

sock_1.bind(('', PORT))
#sock_2.connect((IP2, PORT))

try:
  threading.Thread(target=from_robot, args=(sock_1, sock_2, )).start()
  threading.Thread(target=from_fronius, args=(sock_1, sock_2, )).start()
  
except KeyboardInterrupt:
  conn.close()
  sock_2.close()
  sys.exit()

sock.setblocking(True)
"""
sock_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_1.settimeout(15.0)
sock_2.settimeout(15.0)

sock_1.bind((IP1, PORT))
sock_1.listen(1)
conn, addr = sock_1.accept()

sock_2.connect((IP2, PORT))

try:
  

except KeyboardInterrupt:
  conn.close()
  sock_2.close()
  sys.exit()

sock.setblocking(True)
"""
