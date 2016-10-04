#include <iostream>
#include <cmath>
#include <list>
#include "custom_socket.h"
#include <omp.h>

using namespace std;

static const int MAX_DEPTH = 2 ;
static const int LOOSING_SCORE = -1000 ;
static const int WINNING_SCORE = 1000 ;
static const int WEIGHTS_AVAILABLE = 15 ;
bool player_1_availableweights[WEIGHTS_AVAILABLE + 1] ; // indices 1 to 15 representing weights 1kg..15kg
bool player_2_availableweights[WEIGHTS_AVAILABLE + 1] ; // indices 1 to 15 representing weights 1kg..15kg

class Board {
	public :
		static const int BOARD_LENGTT = 50 ;
		static const int HALF_BOARD_LENGTH = 25;

		static const int INITIAL_BLOCK_WEIGHT = 3 ;
		static const int INITIAL_BLOCK_POSITION = -4 ;
		static const int LEFT_PIVOT_POSITION = -3 ;
		static const int RIGHT_PIVOT_POSITION = -1 ;
		bool weightsRemaining[WEIGHTS_AVAILABLE + 1] ; // indices 1 to 15 representing weights 1kg..15kg
		int boardPositive[HALF_BOARD_LENGTH + 1]; // indices 0 to 25 representing board from -0 to 25
		int boardNegetive[HALF_BOARD_LENGTH + 1]; // indices 1 to 25 representing board from -25 to -1

		float torqueLeftPivot, torqueRightPivot ;
		static const int torqueLeftBoardWeight = -9 ;	//Torque about left pivot due to weight of the board
		static const int torqueRightBoardWeight = 3 ;	//Torque about right pivot due to weight of the board

		void initWeights(){
			for(int i=1;i<=WEIGHTS_AVAILABLE;i++) {
				weightsRemaining[i] = true;
			}
		}
		void initBoard(){
			for(int i=0;i<=HALF_BOARD_LENGTH;i++){
				boardPositive[i] = 0;
				boardNegetive[i] = 0;
			}
			//Placing 3kg block at -4 location
			boardNegetive[abs(INITIAL_BLOCK_POSITION)] = INITIAL_BLOCK_WEIGHT;
		}

		//Constructor
		Board(){
			initWeights();
			initBoard();
			calculateTorques();
		}

		void updateBoard(string * tokens){
			int index ;
			for(int i=1;i<=51;i++){
				index = abs(i - 26);
				if(i<26) {
					if(boardNegetive[index] != stoi(tokens[i])) {
						player_2_availableweights[stoi(tokens[i])] = false;
					}
					boardNegetive[index] = stoi(tokens[i]);
				} else {
					if(boardPositive[index] != stoi(tokens[i])) {
						player_2_availableweights[stoi(tokens[i])] = false;
					}
					boardPositive[index] = stoi(tokens[i]);
				}

			}
		}
		void printBoard(){
			if(true) {
				cout<<"Printing all locations with non zero weights"<<endl;
				for(int i=HALF_BOARD_LENGTH;i>=1;i--){
					if(boardNegetive[i]!=0){
						cout << "position:" << -i << " , weight:" << boardNegetive[i] << endl ;
					}
				}
				for(int i=0;i<=HALF_BOARD_LENGTH;i++){
					if(boardPositive[i]!=0){
						cout << "position:" << i << " , weight:" << boardPositive[i] << endl ;
					}
				}
			}
		}

		//Method to add weight on the board
		//returns true if weight was successfully added
		bool addWeight(int weight, int loc){

			bool addedSuccessfully = false;


			if(loc >=0) {
				if(boardPositive[loc] == 0){
					boardPositive[loc] = weight ;
					//removing weight from available weights
					//weightsRemaining[weight] = false;
					//addedSuccessfully = true ;
					//calculateTorques();
				}

			}else{
				if(boardNegetive[abs(loc)] == 0){
					boardNegetive[abs(loc)] = weight ;
					//removing weight from available weights
					//weightsRemaining[weight] = false;
					//addedSuccessfully = true ;
					//calculateTorques();
				}
			}
			return addedSuccessfully;
		}

		bool removeWeight(int weight, int loc){
			if(loc >=0) {
				if(boardPositive[loc] != 0){
					boardPositive[loc] = 0 ;
					return true;
					//calculateTorques();
				}else{
					return false;
				}

			}else{
				if(boardNegetive[abs(loc)] != 0){
					boardNegetive[abs(loc)] = 0 ;
					//calculateTorques();
					return true;
				}else{
					return false;
				}
			}
		}

		void printRemainingWeights(){
		}

		void calculateTorques() {
			calculateTorqueLeftPivot();
			calculateTorqueRightPivot();
		}

		//if this torque is positive then board is going to tip to left side
		float calculateTorqueLeftPivot() {
			float result = torqueLeftBoardWeight;
			float dist = 0 ;
			float force = 0;

			//for negetive board
			for(int pos = HALF_BOARD_LENGTH; pos >=1 ; pos--){
				if(boardNegetive[pos]!=0){
					force = boardNegetive[pos];
					dist = pos + LEFT_PIVOT_POSITION;
					result = result + force*dist;
				}
			}
			//for positive board
			for(int pos = 0; pos <= HALF_BOARD_LENGTH ; pos++){
				if(boardPositive[pos]!=0){
					force = boardPositive[pos];
					dist = LEFT_PIVOT_POSITION - pos;
					result = result + force*dist;
				}
			}
			torqueLeftPivot = result;
			return torqueLeftPivot;
		}

		//if this torque is positive then board is going to tip to right side
		float calculateTorqueRightPivot() {
			float result = torqueRightBoardWeight;
			float dist = 0 ;
			float force = 0;

			//for negetive board
			for(int pos = HALF_BOARD_LENGTH; pos >=1 ; pos--){
				if(boardNegetive[pos]!=0){
					force = boardNegetive[pos];
					dist = pos + RIGHT_PIVOT_POSITION;
					result = result - force*dist;
				}
			}
			//for positive board
			for(int pos = 0; pos <= HALF_BOARD_LENGTH ; pos++){
				if(boardPositive[pos]!=0){
					force = boardPositive[pos];
					dist = pos - RIGHT_PIVOT_POSITION;
					result = result + force*dist;
				}
			}
			torqueRightPivot = result;

			return torqueRightPivot;
		}

		//return false if by adding this weight board will tip left
		bool canAddWeightTipLeft(int weight, int loc){
			float distFromLeftPivot = loc - LEFT_PIVOT_POSITION ;
			float torqueLeft = weight*distFromLeftPivot;
			if( (calculateTorqueLeftPivot()-torqueLeft)> 0){
				return false;
			} else {
				return true;
			}
		}

		//return false if by adding this weight board will tip right
		bool canAddWeightTipRight(int weight, int loc){
			float distFromRightPivot = loc - RIGHT_PIVOT_POSITION ;
			float torqueRight = weight*distFromRightPivot;
			if( (calculateTorqueRightPivot() + torqueRight)> 0){
				return false;
			}else{
				return true ;
			}
		}

		void getPlayableMoves(bool weightsAvailable[], int myMoves[1000][2], int &length) {
			length = 0;
			for(int i=WEIGHTS_AVAILABLE; i>=1; i--){
				if(weightsAvailable[i]){
					for(int j = -25; j<=25; j++){
						if(canAddWeight(i,j)) {
							myMoves[length][0] = i;
							myMoves[length][1] = j;
							length++;
							//cout<<"getPlayableMoves, weight:"<<i<<" location:"<<j<<endl;
						}
					}
				}
			}
		}

		//return false if after adding this weight board is going to tip
		bool canAddWeight(int weight, int loc) {
			if( (loc>=0 && boardPositive[loc]!=0 ) || (loc<0 && boardNegetive[abs(loc)]!=0)){
				return false;
			}
			return (canAddWeightTipLeft(weight,loc) && canAddWeightTipRight(weight,loc));
		}

		bool hasWeight(int weight) {
			for(int i=HALF_BOARD_LENGTH;i>=1;i--){
					if(boardNegetive[i]==weight){
						return true ;
					}
				}
				for(int i=0;i<=HALF_BOARD_LENGTH;i++){
					if(boardPositive[i]==weight){
						return true ;
					}
				}
				return false;
		}

		int locationOfWeight(int weight) {
			for(int i=HALF_BOARD_LENGTH;i>=1;i--){
					if(boardNegetive[i]==weight){
						return -i ;
					}
				}
				for(int i=0;i<=HALF_BOARD_LENGTH;i++){
					if(boardPositive[i]==weight){
						return i ;
					}
				}
				return 0;
		}

		bool isTippingAfterRemoving(int weight, int loc){
			bool result = true;
			removeWeight(weight,loc);
			if(calculateTorqueLeftPivot() < 0 && calculateTorqueRightPivot() <0){
				result = false;
			}
			addWeight(weight,loc);
			return result;
		}
};

tcp_client c;
int socketNo = 5008;

string* getTokens() {
	string* tokens = new string[53];
	string data;
	while(1) {
		data = c.receive(2048);
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

	tokens[j] = curr[0];
	return tokens;

}

int playAddMove(Board & board, bool player_1_availableweights[], bool player_2_availableweights[], int player, int depth) {
	int length;
	int playableMoves[1000][2];
	if(player == 1){
		board.getPlayableMoves(player_1_availableweights, playableMoves, length);
		if(length==0){
			return LOOSING_SCORE;
		}
		else if(depth==MAX_DEPTH){
			return playableMoves[0][0];
		}
		int maxScore=0;
		int score = 0;
		int weight = playableMoves[0][0];
		int loc = playableMoves[0][0];

		#pragma omp parallel for
		for (int i=0;i<length;i++){
			board.addWeight(playableMoves[i][0],playableMoves[i][1]);
			player_1_availableweights[playableMoves[i][0]] = false ;
			score = playAddMove(board,player_1_availableweights,player_2_availableweights,2, depth+1);
			if(score > maxScore) {
				maxScore =  score ;
				weight = playableMoves[i][0];
				loc = playableMoves[i][1];
			}
			board.removeWeight(playableMoves[i][0],playableMoves[i][1]);
			player_1_availableweights[playableMoves[i][0]] = true ;
			if(maxScore==WINNING_SCORE){
				break;
			}
		}

		string data = to_string((long long)weight) + " " + to_string((long long)loc);
		c.send_data(data);
		player_1_availableweights[weight] = false;
		board.addWeight(weight,loc);
		// cout<<board.calculateTorqueLeftPivot()<<board.calculateTorqueRightPivot()<<endl;
		return maxScore;
	} else if(player==2){
		int score = 0;
		int minScore = 1000;
		board.getPlayableMoves(player_2_availableweights,playableMoves,length);
		if(length==0){
			return WINNING_SCORE;
		}
		#pragma omp parallel for
		for (int i=0;i<length;i++){
    		board.addWeight(playableMoves[i][0],playableMoves[i][1]);
    		player_2_availableweights[playableMoves[i][0]] = false ;
    		int score = playAddMove(board,player_1_availableweights,player_2_availableweights,1, depth+1);
    		board.removeWeight(playableMoves[i][0],playableMoves[i][1]);
    		player_2_availableweights[playableMoves[i][0]] = true ;
    		if(score <minScore) {
    			minScore = score;
    		}
    	}
    	return minScore;
	}
}

void playRemoveMove(Board & board){
	bool weightFound = false;
	for (int i = 1; i <= 15; i++)
	{
		if(board.hasWeight(i)){
			int loc = board.locationOfWeight(i);
			if(!board.isTippingAfterRemoving(i,loc)) {
				board.removeWeight(i,loc);
				// cout<<board.calculateTorqueLeftPivot()<<board.calculateTorqueRightPivot()<<endl;
				cout<<loc<<endl;
				string data = to_string((long long)loc);
    			c.send_data(data);
    			weightFound = true;
				break;
			}
		}
	}
	if(!weightFound) {
		for (int i = 1; i <= 15; i++)
	{
		if(board.hasWeight(i)){
			int loc = board.locationOfWeight(i);
			board.removeWeight(i,loc);
			// cout<<board.calculateTorqueLeftPivot()<<board.calculateTorqueRightPivot()<<endl;
			string data = to_string((long long)loc);
    		c.send_data(data);
			break;
		}
	}
	}
}

int main(){
	Board mBoard;
	for (int i = 1; i <= WEIGHTS_AVAILABLE; i++)
	{
		player_1_availableweights[i] = true ;
		player_2_availableweights[i] = true ;
	}
	mBoard.printBoard();

	cout << "Enter Portnumber:" ;
	cin >> socketNo ;
	c.conn("localhost", socketNo);
	string * tokens = getTokens();

	while(tokens[52]=="0") {
		mBoard.updateBoard(tokens);
		if(tokens[0]=="1") {
			playAddMove(mBoard,player_1_availableweights,player_2_availableweights,1,0);
		} else if(tokens[0]=="2"){
			playRemoveMove(mBoard);
		}
		tokens = getTokens();
	}


	c.closeconn();
	return 0;
}
