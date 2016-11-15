from person import Person
from matchmaker import Matchmaker
import socket
import utils
import numpy as np

class IO:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', port))

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
            data = self.sock.recv(8*self.numAttr)
            print('%d: Received guess = %r' % (i, data))
            assert data[-1] == '\n'
            self.sock.send(utils.floats_to_msg2(self.player.getNewWeights(data)))

    def startMatchmakerIO(self):
        candidates = []
        for i in range(20):
            # score digits + binary labels + commas + exclamation
            data = self.sock.recv(8 + 2*self.numAttr)
            print('Score = %s' % data[:8])
            assert data[-1] == '\n'
            candidates.append(utils.parseCandidateData(data))

        self.player.parseInitialData(candidates)

        # Set initial score higher than 1 so we know it is initial round
        score = 2
        candidate = []
        for i in range(20):
            candidate = self.player.guess(candidate, score, i)
            self.sock.sendall(utils.floats_to_msg4(candidate))

            data = self.sock.recv(8)
            assert data[-1] == '\n'
            score = float(data[:-1])

            # if np.isclose(score, 1):
            #     break

            print('i = %d score = %f' % (i, score))
