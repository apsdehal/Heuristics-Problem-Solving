#include <iostream>
#include <utility>
#include <map>
#include <string>
#include "custom_socket.h"

using namespace std;

typedef pair<int, int> pii;

class ExpandingNim {
	private:
		map<pii, bool> mem;
		int currentMax;
		int nStones;
		int currentStones;
		bool opponentResetState;
		bool hasOpponentUsedReset;
		bool myResetState;
		tcp_client c;
	public:
		ExpandingNim(int nStones = 100, int curr = 2, int socketNo = 50008) {
			this->nStones = nStones;
			this->currentMax = curr;
			this->isWinning(nStones, curr);
			this->currentStones = nStones;
			this->opponentResetState = 0;
			this->myResetState = 0;
			this->hasOpponentUsedReset = 0;
			c.conn("localhost", socketNo);
		}

		void setCurrentMax(int curr) {
			this->currentMax = curr;
		}

		int isWinning(int n, int currMax) {
			if (n <= 0) {
				return 0;
			}
			pii curr = make_pair(n, currMax);

			if (mem.find(curr) != mem.end()) {
				return mem[curr];
			}

			int lose = 0;
			for(int i = 1; i < currMax + 2; i++) {
				if (i == currMax + 1) {
					if (!isWinning(n - i, currMax + 1)) {
						lose = 1;
					}
				} else {
					if (!isWinning(n - i, currMax)) {
						lose = 1;
					}
				}
			}

			if (lose == 1) {
				// Okay we lose means atleast we have chance of winning
				mem[curr] = 1;
			} else {
				mem[curr] = 0;
			}

			return lose;
		}

		void printSpace() {
			map<pii, bool>::iterator it;
			for(it = mem.begin(); it != mem.end(); it++) {
				cout<<((*it).first.first)<<" "<<((*it).first.second)<<" "<<((*it).second ? "Win" : "Lose")<<endl;
			}
		}

		pii calculateNextMove() {
			cout<<(mem[make_pair(this->currentStones, this->currentMax)] ? "I am winning" : "I am losing")<<endl;
			int bestMove = 1; int reset = 0;
			int originalCurrentMax = this->currentMax;

			if (this->hasOpponentUsedReset) {
				this->hasOpponentUsedReset = 0;
				this->opponentResetState = 1;
				this->currentMax = 2;
			}

			for(int i = 1; i <= this->currentMax + 1; i++) {
				if (this-> currentStones - i  <= 0) {
					bestMove = i;
					break;
				}

				if (i == this->currentMax + 1) {
					if (!mem[make_pair(this->currentStones - i, i)]) {
						bestMove = i;
					}
				} else {
					if (!mem[make_pair(this->currentStones - i, this->currentMax)]) {
						bestMove = i;
					}
				}
			}

			this->currentMax = originalCurrentMax;

			if (bestMove == this->currentMax + 1) {
				this->currentMax = this->currentMax + 1;
			}

			if ((this->currentStones - bestMove) <= (this->currentMax + 1)
				&& this->opponentResetState && !this->myResetState) {
				reset = 1;
				this->myResetState = 1;
			}

			return make_pair(bestMove, reset);
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

		void update() {
			cout<<"Updating state"<<endl;
			string* tokens = this->getTokens();

			this->currentStones = stoi(tokens[0]);
			this->currentMax = stoi(tokens[1]);
			this->hasOpponentUsedReset = tokens[2] == "0" ? 0 : 1;

			if (this->hasOpponentUsedReset) {
				cout<<"Opponent has used reset"<<endl;
			}

			cout<<"Current left stones are "<<this->currentStones<<endl;
			cout<<"CurrentMax is "<<this->currentMax<<endl;

			if (tokens[3] == "1") {
				cout<<"Connection closed, dying"<<endl;
				this->c.closeconn();
			}
		}

		void play() {
			bool flag = 0;

			while(this->currentStones > 0) {
				if (flag) {
					pii nextMove = this->calculateNextMove();

					cout<<"My next move is "<<nextMove.first<<endl;
					this->currentStones = this->currentStones - nextMove.first;

					if (nextMove.second == 1) {
						cout<<"Going to use reset"<<endl;
					}

					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					string toBeSend = to_string(nextMove.first) + " " + to_string(nextMove.second);
					c.send_data(toBeSend);
					flag = 0;
				} else {
					cout<<"Opponent's move"<<endl;
					this->update();
					flag = 1;
				}
			}
			cout<<(flag ? "Lose" : "Won")<<endl;
			this->c.closeconn();
		}

		void playManually() {
			bool flag = 0;
			while(this->currentStones > 0) {
				if (flag) {
					cout<<(mem[make_pair(this->currentStones, this->currentMax)] ? "You are winning" : "You are losing")<<endl;
					int nextMove, reset;
					cout<<"Your move"<<endl;
					cin>>nextMove>>reset;

					if (nextMove == this->currentMax + 1) {
						this->currentMax = this->currentMax + 1;
					}
					this->currentStones = this->currentStones - nextMove;

					string toBeSend = to_string(nextMove) + " " + to_string(reset);
					c.send_data(toBeSend);

					if (reset) {
						cout<<"You have used reset"<<endl;
					}
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 0;
				} else {
					cout<<"Opponent's move"<<endl;
					this->update();
					flag = 1;

				}
			}
			cout<<(flag ? "Won" : "Lose")<<endl;
			this->c.closeconn();
		}

		void playTogether() {
			bool flag = 0;

			while(this->currentStones > 0) {
				if (flag) {
					cout<<(mem[make_pair(this->currentStones, this->currentMax)] ?
					"I am winning" : "I am losing")<<endl;

					pii nextMove = this->calculateNextMove();

					cout<<"My next move is "<<nextMove.first<<endl;
					this->currentStones = this->currentStones - nextMove.first;

					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;

					flag = 0;
				} else {
					cout<<(mem[make_pair(this->currentStones, this->currentMax)] ?
					"Opponent is winning" : "Opponent is losing")<<endl;

					pii nextMove = this->calculateNextMove();

					cout<<"Opponent's next move is "<<nextMove.first<<endl;
					this->currentStones = this->currentStones - nextMove.first;
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 1;
				}
			}
			cout<<(flag ? "Lose" : "Won")<<endl;
			this->c.closeconn();
		}
};

int main() {
	int n, type;
	cout<<"How do you want to play?"<<endl<<"1. Bot\n"<<"2. Manually\n"
	<<"3. Bot against Bot"<<"\n4. Print Space"<<endl;
	cin>>type;
	cout<<"Enter number of stones:"<<endl;
	cin>> n;

	int socketNo;

	if (type != 4) {
		cout<<"Enter socket no"<<endl;
		cin>>socketNo;
	}

	if (!socketNo) {
		socketNo = 50008;
	}

	ExpandingNim *obj = new ExpandingNim(n, 2, socketNo);

	if (type == 1) {
		obj->play();
	} else if (type == 2) {
		obj->playManually();
	} else if (type == 3) {
		obj->playTogether();
	} else {
		obj->printSpace();
	}

	return 0;
}
