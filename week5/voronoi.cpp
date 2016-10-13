#include <iostream>
#include "custom_socket.h"

using namespace std;

const int MAX_POINTS = 1000 ;
const int MAX_STONES_POSSIBLE = 15;
const int OPPONENT = -1 ;
const int PLAYER = 1;
float pull[MAX_POINTS][MAX_POINTS];
int maxStones = 0;
tcp_client c;
int socketNo = 9000;

void initPull();
string * getTokens();
void updateOpponentMove(int,int);
void updatePull(int,int,int);
string makeMove();
pair<int,int> calcScore();
bool feasibleMove(int,int);
int calcScoreByEvaluatingMove(int,int);

int noOfMoves = 0;
int lastMoveOfOpponet_x = 0;
int lastMoveOfOpponet_y = 0;
int myMoves = 0;
int opponentMoves = 0;
pair<int,int> myStonePositions[MAX_STONES_POSSIBLE];
pair<int,int> opponentStonePositions[MAX_STONES_POSSIBLE];

int main(int argc, char *argv[]){
	//Initializations
	c.conn("localhost", socketNo);
	initPull();
	if(argc!=2){
		cout << "Some error passing value of number of stones." <<endl ;
		return 0;
	}else {
		maxStones = stoi(argv[1]);
		cout << "Number of stones:" << maxStones <<endl;
	}
	//data to be read from server
	string *data;
	string myMove="";

	//putting in infinite loop till server signals that game has ended
	while(true){
		data = getTokens();
		//check if game has ended
		if (stoi(data[0]) == 1){
			break;
		}
		noOfMoves = stoi(data[1]) - 1;
		if(noOfMoves>=0){
			lastMoveOfOpponet_x = stoi(data[2 + noOfMoves*3]);
			lastMoveOfOpponet_y = stoi(data[2 + noOfMoves*3 + 1]);
			//updateOpponentMove(lastMoveOfOpponet_x,lastMoveOfOpponet_y);
		}
		myMove = makeMove();
		c.send_data(myMove) ;
		myMoves++ ;
	}
	cout << "game has ended" <<endl;

	c.closeconn();
	return 0;
}

string* getTokens() {
	string* tokens = new string[4];
	string data;
	while(1) {
		data = c.receive(1024);
		if (data.length() > 0) {
			break;
		}
	}

	string curr = "";

	int j = 0;

	for(int i = 0; i < data.length(); i++) {
		if (data[i] == ' ') {
			tokens[j] = curr;
			curr = "";
			j++;
		} else {
			curr += data[i];
		}
	}

	tokens[j] = curr;
	return tokens;

}
void initPull() {
	for (int i = 0; i < MAX_POINTS; i++)
	{
		for (int j = 0; j < MAX_POINTS; j++)
		{
			pull[i][j] = 0;
		}
	}
}

void updateOpponentMove(int x, int y){
	opponentStonePositions[opponentMoves] = make_pair(x,y) ;
	opponentMoves++ ;
	updatePull(x,y,OPPONENT);
}

void updatePull(int x, int y, int who){
	if(who==OPPONENT){
		for (int i = 0; i < MAX_POINTS; ++i)
		{
			for (int j = 0; i < MAX_POINTS; ++j)
			{
				int xDist = abs(x-i);
				int yDist = abs(y-j);
				int dist = xDist + yDist;
				if(dist!=0) {
					pull[i][j] = pull[i][j] - 1/dist;
				}
			}
		}
	}

}

string makeMove(){
	int maxScore = 0;
	int score = 0;
	int x=0,y=0;
	string move = "";
	for (int i = 0; i < MAX_POINTS; ++i)
	{
		for (int j = 0; j < MAX_POINTS; ++j)
		{
			if(pull[i][j] < 0) {
				if(feasibleMove(i,j)) {
					score = calcScoreByEvaluatingMove(i,j);
					if(score > maxScore){
						maxScore = score;
						x = i;
						y = j;
					}
				}
			}
		}
	}
	return to_string(x) + " " + to_string(y);
}

pair<int,int> calcScore(){
	int myScore = 0;
	int opponentScore = 0;
	for (int i = 0; i < MAX_POINTS; ++i)
	{
		for (int j = 0; j < MAX_POINTS; ++j)
		{
			if(pull[i][j] > 0){
				myScore++;
			} else if(pull[i][j] < 0) {
				opponentScore++;
			}
		}
	}
	return make_pair(myScore,opponentScore);
}

int calcScoreByEvaluatingMove(int x,int y) {
	int score = 0;
	int xDist = 0;
	int yDist = 0;
	int dist = 0;
	for (int i = 0; i < MAX_POINTS; ++i)
	{
		for (int j = 0; j < MAX_POINTS; ++j)
		{
			if(pull[i][j] > 0){
				score++;
			} else {
				xDist = abs(x-i);
				yDist = abs(y-j);
				dist = xDist + yDist;
				if(dist!=0 && (pull[i][j] + 1/dist) > 0) {
					score++;
				}
			}
		}
	}
	return score;
}

bool feasibleMove(int x,int y){
	return true;
}