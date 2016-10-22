import socket
from hunter import Hunter

class IO:
    HOST = 'localhost'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    teamname = 'jeopardy'
    def __init__(self, port):
        self.portNo = port
        self.s.connect(self.HOST, self.portNo)

    def start(self):
        prev = "";
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
                self.player = Hunter()
                self.playerType = 'hunter'
                continue
            elif 'prey' in currResp:
                self.player = Prey()
                self.playerType = 'prey'
                continue

            currResp = currResp.split(' ')

            self.player.move(currResp)
