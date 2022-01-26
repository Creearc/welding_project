import sys
import socket
import threading
import time

lock = threading.Lock()

def from_robot(server, client):
  while True:
    res = server.recv(1024)
    client.send(res)
    print('____________\nfrom Robot {}\n'.format(res))

def from_fronius(server, client):
  while True:
    data = client.recv(1024)
    server.send(data)
    print('____________\nfrom Fronius {}\n'.format(data))

    


PORT = 44818
IP1 = ''
IP2 = '192.168.0.2'

connections = []

max_connections = 10
sock_1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_1.bind((IP1, PORT))
sock_1.listen(max_connections)

for i in range(max_connections):
  server, addr = sock_1.accept()
  client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client.connect((IP2, PORT))
  
  threading.Thread(target=from_robot, args=(server, client, )).start()
  threading.Thread(target=from_fronius, args=(server, client, )).start()


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
