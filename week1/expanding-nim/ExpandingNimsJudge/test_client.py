# Echo client program
import socket
import time

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while(1):
    data = s.recv(1024)
    while not data:
        continue
    data = [int(data.split(' ')[i]) for i in [0,1,2,3]]
    if data[3] == 1:
        break
    #put your game logic here
    stonesToDraw = 1
    resetBit = 0
    s.sendall('{} {}'.format(stonesToDraw, resetBit))
s.close()
