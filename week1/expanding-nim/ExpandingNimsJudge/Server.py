import socket

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySocket.bind((self.host, self.port))
        self.connection = [None, None]
        self.address = [None, None]

    def establishConnection(self):
        self.mySocket.listen(2)
        print "Waiting for player 0."
        self.connection[0], self.address[0] = self.mySocket.accept()
        print "Connection from player 0 established."
        print "Waiting for player 1."
        self.connection[1], self.address[1] = self.mySocket.accept()
        print "Connection from player 1 established."

    def send(self, string, player):
        self.connection[player].sendall(string)

    def receive(self, player):
        while(1):
            data = self.connection[player].recv(1024)
            while not data:
                continue
            return data
