import sys
from helpers.io import IO

if __name__ == '__main__':
    port = int(sys.argv[1]) if sys.argv[1] != None else 5000
    ioObj = IO(port)
    ioObj.start()
