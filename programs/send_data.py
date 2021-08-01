import socket
import time

sock = socket.socket()
sock.connect(('127.0.0.1', 9090))



while True:
   sock.send(b'hello, world!')
   print(sock.recv(1024))
   time.sleep(0.5)
   
sock.close()

