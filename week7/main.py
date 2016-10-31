from helpers.io import IO
import sys

if __name__ == '__main__':
    io = IO("localhost", sys.argv[3], int(sys.argv[4]))

    playerName = "choreo" if int(sys.argv[1]) == 1 else "spoiler"
    io.parseInput(sys.argv[2], playerName)

    io.begin()
