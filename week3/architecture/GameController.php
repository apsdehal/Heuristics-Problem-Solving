<?php
class GameController
{
    private $socket;
    private $resources;

    function __construct($address, $port)
    {
        $this->socket = socket_create(AF_INET, SOCK_STREAM, 0);
        socket_bind($this->socket, $address, $port);
    }

    function createConnection()
    {
        socket_listen($this->socket);
        echo "Waiting for Player 1\n";
        while (1) {
            if ($this->resources[1] = socket_accept($this->socket)) {
                echo $this->resources[1];
                socket_set_nonblock($this->resources[1]);
                echo "Connection from Player1 established\n";
                break;
            }
        }

        echo "Waiting for Player 2\n";
        while (1) {
            if ($this->resources[2] = socket_accept($this->socket)) {
                echo $this->resources[2];
                socket_set_nonblock($this->resources[2]);
                echo "Connection from Player2 established\n";
                break;
            }
        }
    }

    function closeConnection()
    {
        socket_close($this->resources[1]);
        socket_close($this->resources[2]);
        socket_close($this->socket);
    }

    function send($player, $string)
    {
        socket_write($this->resources[$player], $string);
    }

    function recv($player)
    {
        while (true) {
            $data = socket_read($this->resources[$player], 1024, PHP_BINARY_READ);
            if ($data != "") {
                echo $data;
                return $data;
            }
        }
    }
}
