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
		tcp_client c;
	public:
		ExpandingNim(int nStones, int curr = 2) {
			this->nStones = nStones;
			this->currentMax = curr;
			this->isWinning(nStones, curr);
			this->currentStones = nStones;
			c.conn("localhost", 50008);
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

		int calculateNextMove() {
			int bestMove = 1;
			for(int i = 1; i <= this->currentMax + 1; i++) {
				if (this-> currentStones - i  <= 0) {
					return i;
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

			if (bestMove == this->currentMax + 1) {
				this->currentMax = this->currentMax + 1;
			}
			return bestMove;
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

			cout<<"Current left stones are "<<this->currentStones<<endl;
			cout<<"CurrentMax is "<<this->currentMax<<endl;
		}
		void play() {
			bool flag = 0;

			while(this->currentStones > 0) {
				if (flag) {
					int nextMove = this->calculateNextMove();

					cout<<"My next move is "<<nextMove<<endl;
					this->currentStones = this->currentStones - nextMove;
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					string toBeSend = to_string(nextMove) + " 0";
					c.send_data(toBeSend);
					flag = 0;
				} else {
					cout<<"Opponent's move"<<endl;
					this->update();
					flag = 1;
				}
			}
			cout<<(flag ? "Lose" : "Won")<<endl;
		}

		void playManually() {
			bool flag = 0;
			while(this->currentStones > 0) {
				if (flag) {
					int nextMove;
					cout<<"Your move"<<endl;
					cin>>nextMove;

					if (nextMove == this->currentMax + 1) {
						this->currentMax = this->currentMax + 1;
					}
					this->currentStones = this->currentStones - nextMove;

					string toBeSend = to_string(nextMove) + " 0";
					c.send_data(toBeSend);

					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 0;
				} else {
					cout<<"Opponent's move"<<endl;
					this->update();
					flag = 1;

				}
			}
		}

		void playTogether() {
			bool flag = 0;

			while(this->currentStones > 0) {
				if (flag) {
					cout<<(mem[make_pair(this->currentStones, this->currentMax)] ?
					"I am winning" : "I am losing")<<endl;

					int nextMove = this->calculateNextMove();

					cout<<"My next move is "<<nextMove<<endl;
					this->currentStones = this->currentStones - nextMove;
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 0;
				} else {
					cout<<(mem[make_pair(this->currentStones, this->currentMax)] ?
					"Opponent is winning" : "Opponent is losing")<<endl;
					int nextMove = this->calculateNextMove();
					cout<<"Opponent's next move is "<<nextMove<<endl;
					this->currentStones = this->currentStones - nextMove;
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 1;
				}
			}
			cout<<(flag ? "Lose" : "Won")<<endl;
		}
};

int main() {
	int n, type;
	cout<<"How do you want to play?"<<endl<<"1. Bot\n"<<"2. Manually\n"<<"3. Bot against Bot"<<endl;
	cin>>type;
	cout<<"Enter number of stones:"<<endl;
	cin>> n;

	ExpandingNim *obj = new ExpandingNim(n);
	// obj->printSpace();
	// return 0;

	if (type == 1) {
		obj->play();
	} else if (type == 2) {
		obj->playManually();
	} else {
		obj->playTogether();

	}

	return 0;
}
