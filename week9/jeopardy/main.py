# from helpers.io import IO
import sys

if __name__ == '__main__':
    io = IO("localhost", int(sys.argv[2]))

    playerName = "person" if int(sys.argv[1]) == 0 else "matchmaker"
    io.start(playerName)

    io.begin()
