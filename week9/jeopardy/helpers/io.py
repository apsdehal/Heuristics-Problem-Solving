from person import Person
from matchmaker import Matchmaker
import socket

class IO:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', PORT))

    def start(self, playerName):
        numString = self.sock.recv(4)
        assert numString.endswith('\n')

        numAttr = int(numString[:-1])
        self.numAttr = numAttr

        if playerName == 'person':
            self.player = Person(numAttr)
            self.startPersonIO()
        elif playerName == 'matchmaker':
            self.player = Matchmaker(numAttr)
            self.startMatchmakerIO()

        self.sock.close()

    def startPersonIO(self):
        initialWeights = self.player.getValidWeights()
        idealCandidate = self.player.getIdealCandidate()
        antiIdealCandidate = self.player.getAntiIdealCandidate()

        self.sock.sendall(utils.floats_to_msg2(initialWeights))

        self.sock.sendall(utils.candidate_to_msg(idealCandidate))
        self.sock.sendall(utils.candidate_to_msg(antiIdealCandidate))


        for i in range(20):
            # 7 char weights + commas + exclamation
            data = sock.recv(8*num_attr)
            print('%d: Received guess = %r' % (i, data))
            assert data[-1] == '\n'
            sock.send(floats_to_msg2(self.player.getNewWeights(data)))
