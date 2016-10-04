# Echo client program
import socket
import sys
import random
HOST = 'localhost'    # The remote host
PORT = int(sys.argv[1])              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
myWeight = dict()
for i in range(1, 16):
    myWeight[i] = 1;


def check_balance(board):
    left_torque = 0
    right_torque = 0
    for i in range(0,51):
        left_torque += (i - 25 + 3) * board[i]
        right_torque += (i - 25 + 1) * board[i]
    left_torque += 3 * 3
    right_torque += 1 * 3
    return left_torque >= 0 and right_torque <= 0


def find_place_position(key, board):
    for i in range(0,26):
        if board[i] == 0:
            board[i] = key
            if check_balance(board):
                board[i] = 0
                return i
            board[i] = 0
        if board[50-i] == 0:
            board[50-i] = key
            if check_balance(board):
                board[50 - i] = 0
                return 50-i
            board[50-i] = 0
    return -100

while(1):
    data = s.recv(1024)
    while not data:
        continue
    data = [int(data.split(' ')[i]) for i in range(0, 53)]
    board = data[1:-1]
    check_balance(board)
    #print board
    if data[52] == 1:
        break

    if data[0] == 1:
        allPosition = []
        for key,value in myWeight.iteritems():
            if value == 1:
                position = find_place_position(key, board)
                if position != -100:
                    allPosition.append((key, position - 25))
                if position != -100:
                    allPosition.append((key, position - 25))
                    break
        if len(allPosition) == 0:
            choice = (1, 0)
        else:
            choice = random.choice(allPosition)
        myWeight[choice[0]] = 0
        print choice
        s.sendall('{} {}'.format(choice[0], choice[1]))

    else:
        allPossiblePosition = []
        for i in range(0, 51):
            if board[i] != 0:
                tempWeight = board[i]
                board[i] = 0
                if check_balance(board):
                    allPossiblePosition.append(i - 25)
                board[i] = tempWeight
        if len(allPossiblePosition) == 0:
            choice = (1)
        else:
            choice = random.choice(allPossiblePosition)
            random.jumpahead(1);
        ##print choice
        s.sendall('{}'.format(choice))


s.close()
