import socket
from hunter import Hunter

class IO:
    HOST = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teamname = 'jeopardy'
    def __init__(self, port):
        prev = ""
        self.flag = 0
        self.portNo = port
        self.s.connect(self.HOST, self.portNo)

    def start(self):
        while 1:
            resp = self.s.recv(1024) + prev

            if '\n' not in resp:
                prev = resp
                continue

            resp = resp.split('\n')

            currResp = resp[0]
            resp.pop(0)

            prev = '\n'.join(resp)

            if 'sendname' in currResp:
                self.s.sendall(self.teamname)
                continue

            if 'hunter' in currResp:
                self.playerType = 'hunter'
                continue
            elif 'prey' in currResp:
                self.playerType = 'prey'
                continue

            currResp = currResp.split(' ')

            currResp = self.parseInput(currResp)

            if self.flag == 0:
                self.flag = 1
                self.player = Hunter(currResp) if self.playerType == 'hunter' else Prey(currResp)
            else:
                self.sendall(self.player.move(currResp))

    def parseInput(self, resp):
        info = {};

        info['timeLeft'] = resp[0]
        info['gameNum'] = resp[1]
        info['tickNum'] = resp[2]

        info['maxWalls'] = resp[3]
        info['wallPlacementDelay'] = resp[4]
        info['boardSizeX'] = resp[5]
        info['boardSizeY'] = resp[6]
        
