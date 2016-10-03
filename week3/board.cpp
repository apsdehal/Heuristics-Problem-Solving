#include <iostream>
#include <cmath>
#include "mUtils.h"
using namespace std;

class Board {
	public :
		static const int BOARD_LENGTT = 50 ;
		static const int HALF_BOARD_LENGTH = 25;  
		static const int WEIGHTS_AVAILABLE = 15 ;
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
		void printBoard(){
			if(LOGS_ENABLED) {
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

			if(loc > HALF_BOARD_LENGTH || loc < -HALF_BOARD_LENGTH) {
				if(LOGS_ENABLED){
					cout << "Class: Board.cpp, method:addWeight(), location out of bound, " ;
					cout <<"weight:" << weight <<", location:" << loc << endl;
				}
				return false;
			}
			//the weight should be less than max available weights
			if( weight > WEIGHTS_AVAILABLE){
				if(LOGS_ENABLED){
					cout << "Class: Board.cpp, method:addWeight(), weight out of bound, " ;
					cout <<"weight:" << weight <<", location:" << loc << endl;
				}
				return false;
			}
			//check if weight is available
			if(!weightsRemaining[weight]){
				if(LOGS_ENABLED){
					cout << "Class: Board.cpp, method:addWeight(), weight not available, ";
					cout <<"weight:" << weight <<", location:" << loc << endl;
				}
				return false;
			}


			if(loc >=0) {
				if(boardPositive[loc] == 0){
					boardPositive[loc] = weight ;
					//removing weight from available weights
					weightsRemaining[weight] = false;
					addedSuccessfully = true ;
					calculateTorques();
				}else{
					if(LOGS_ENABLED) {
						cout << "Class: Board.cpp, method:addWeight(), cannot add weight, position:"<<loc << endl;
					}
				}

			}else{
				if(boardNegetive[abs(loc)] == 0){
					boardNegetive[abs(loc)] = weight ;
					//removing weight from available weights
					weightsRemaining[weight] = false;
					addedSuccessfully = true ;
					calculateTorques();
				}else{
					if(LOGS_ENABLED) {
						cout << "Class: Board.cpp, method:addWeight(), cannot add weight, position:"<<loc << endl;
					}
				}
			}
			return addedSuccessfully;
		}

		void printRemainingWeights(){
			if(LOGS_ENABLED){
				for(int i=1;i<=WEIGHTS_AVAILABLE;i++) {
					if(weightsRemaining[i])
					cout << "weight:" << i  <<endl;
				}
			}
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
			if(LOGS_ENABLED){
				cout<< "torqueLeftPivot:" << torqueLeftPivot << endl;
			}
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
			if(LOGS_ENABLED){
				cout<< "torqueRightPivot:" << torqueRightPivot << endl;
			}
			return torqueRightPivot;
		}

		//return false if by adding this weight board will tip left
		bool canAddWeightTipLeft(int weight, int loc){
			float distFromLeftPivot = loc - LEFT_PIVOT_POSITION ;
			float torqueLeft = weight*distFromLeftPivot;
			if( (torqueLeftPivot-torqueLeft)> 0){
				if(LOGS_ENABLED){
					cout<< "Cannot add weight, board will tip left. weight:";
					cout << weight << " ,location:" << loc << endl;
				}
				return false;
			} else {
				return true;
			}
		}

		//return false if by adding this weight board will tip right
		bool canAddWeightTipRight(int weight, int loc){
			float distFromRightPivot = loc - RIGHT_PIVOT_POSITION ;
			float torqueRight = weight*distFromRightPivot;
			if( (torqueRightPivot + torqueRight)> 0){
				if(LOGS_ENABLED){
					cout<< "Cannot add weight, board will tip right. weight:";
					cout << weight << " ,location:" << loc << endl;
				}
				return false;
			}else{
				return true ;
			}
		}

		//return false if after adding this weight board is going to tip
		bool canAddWeight(int weight, int loc) {
			if(!weightsRemaining[weight]){
				if(LOGS_ENABLED){
					cout<< "Cannot add weight, weight is not avavilable. weight:";
					cout << weight << " ,location:" << loc << endl;
				}
				return false;
			}
			if( (loc>=0 && boardPositive[loc]!=0 ) || (loc<0 && boardNegetive[abs(loc)]!=0)){
				if(LOGS_ENABLED){
					cout<< "Cannot add weight, location is already filled. weight:";
					cout << weight << " ,location:" << loc << endl;
				}
				return false;
			}
			return (canAddWeightTipLeft(weight,loc) && canAddWeightTipRight(weight,loc));
		}
};

int main(){
	Board mBoard ;
	if(mBoard.canAddWeight(1,1))
	mBoard.addWeight(1,1);
	if(mBoard.canAddWeight(2,-4))
	mBoard.addWeight(2,-4);
	if(mBoard.canAddWeight(3,-8))
	mBoard.addWeight(3,-8);
	if(mBoard.canAddWeight(2,-1))
	mBoard.addWeight(2,-1);
	if(mBoard.canAddWeight(4,4))
	mBoard.addWeight(4,4);
	if(mBoard.canAddWeight(5,5))
	mBoard.addWeight(5,5);

	return 0;
}