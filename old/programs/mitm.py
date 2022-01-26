import sys
import socket

PORT = 9090
IP1 = ''
IP2 = '127.0.0.1'


sock_1 = socket.socket()
sock_2 = socket.socket()

sock_1.bind((IP1, PORT))
sock_1.listen(1)
conn, addr = sock_1.accept()

sock_2.connect((IP2, PORT+1))

try:
  while True:
    print('________________________________________________')
    data = conn.recv(1024)
    print(data)
    sock_2.send(data)
    data = sock_2.recv(1024)
    print(data)
    conn.send(data)

except KeyboardInterrupt:
  conn.close()
  sock_2.close()
  sys.exit()
