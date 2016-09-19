#include <iostream>
#include <utility>
#include <map>

using namespace std;

typedef pair<int, int> pii;

class ExpandingNim {
	private:
		map<pii, bool> mem;
		int currentMax;
		int nStones;
		int currentStones;
	public:
		ExpandingNim(int nStones, int curr = 2) {
			this->nStones = nStones;
			this->currentMax = curr;
			this->isWinning(nStones, curr);
			this->currentStones = nStones;
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

		void play(bool flag = 1) {

			while(this->currentStones > 0) {
				if (flag) {
					int nextMove = this->calculateNextMove();

					cout<<"My next move is "<<nextMove<<endl;
					this->currentStones = this->currentStones - nextMove;
					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 0;
				} else {
					int nextMove;
					cout<<"Opponent's move"<<endl;
					cin>>nextMove;

					if (nextMove == this->currentMax + 1) {
						this->currentMax = this->currentMax + 1;
					}
					this->currentStones = this->currentStones - nextMove;

					cout<<"Current left stones are "<<this->currentStones<<endl;
					cout<<"CurrentMax is "<<this->currentMax<<endl;
					flag = 1;
				}
			}
			cout<<(flag ? "Lose" : "Won")<<endl;
		}

		void playTogether(bool flag = 1) {

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
	int n;
	cin>> n;

	ExpandingNim *obj = new ExpandingNim(n);
	obj->printSpace();
	return 0;
	bool flag;

	cout<<"Who plays first? 1 for you and 0 for opponent"<<endl;

	cin>>flag;

	// obj->playTogether(flag);

	return 0;
}
