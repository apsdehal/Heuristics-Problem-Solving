Input format, output format, and general series of events in the game. 

1. Connection is established between the server and both parties. Please make sure that your code can be run with the port number as a command line argument, which will be provided on the day of the competition.
2. In each turn the server sends a string of the form 'a b c d' (without quotes) where a, b, c, d are integers, 0<a<=100, 2<=b<=100 (well, actually 20, but why?), 0<=c<=1, 0<=d<=1. a denotes the number of stones left, b denotes the maximum of 2 and the maximum stones drawn by either player so far in the game, c denotes if the other player has used the reset bit (by default 0 for player 0 on the first turn), and d denotes the game state (0 means the game has NOT ended, 1 means the game has ended)
3. The server, after sending the string to a player, waits for a response from the player. The response has to be of the form 'x y' (without quotes) where x and y are integers and x denotes the number of stones the player wishes to remove and y denotes if the player wants to use reset. In all cases 1<=x<=b+1 and in the special case of c == 1, 1<=x<=3. Also, 0<=y<=1. After sending the response to the server, the player is expected to keep monitoring the socket for data from the server for the next turn. 
4. The above steps are repeated till either all stones vanish (One of the players achieved a legal win), or either player makes an invalid move or either player times out. 
5. If the game ends at any point, both players receive '0 0 0 1' (without quotes) from the server, and are expected to close the socket and exit cleanly. 

Additional notes:

Timekeeping - Once connection with both players is established, the server sends player 0 the initial number of stones, the default currentmax (2), default reset bit (0), and default game state(0), and notes the time. The server waits for a response from player 0. As soon as a response is received, it updates the total time taken by player 0, and sends the new game state to player 1. 

Idling - At the start of the game, as soon as player 0 makes a connection with the server, it should start monitoring the socket for data from the server. In each subsequent turn, the player is expected to monitor the socket for data from the server as soon as the player sends his move for that turn. (Inadequacy? Or feature to ensure you don't compute things in the background while waiting for the other player's turn?)

Current Max - At any turn, unless the other person has used a reset bit, you can choose to remove any number of stones between 1 and current max + 1. 
Reset - The reset option is NOT a hard reset, that is, it does NOT reset the current max. It forces the opponent to remove 1 or 2 or 3 stones in the NEXT TURN ONLY.

If you have questions/ notice we have missed something, please let us know at dt1295@nyu.edu and pks329@nyu.edu
