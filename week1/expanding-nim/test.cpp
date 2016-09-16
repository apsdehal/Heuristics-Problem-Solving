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
	public:
		ExpandingNim(int nStones, int curr = 2) {
			this->nStones = nStones;
			this->currentMax = curr;
			this->isWinning(nStones, curr);
		}

		void setCurrentMax(int curr) {
			this->currentMax = curr;
		}

		int isWinning(int n, int currentMax) {
			if (n <= 0) {
				return 0;
			}
			pii curr = make_pair(n, currentMax);

			if (mem.find(curr) != mem.end()) {
				return mem[curr];
			}

			int lose = 0;
			for(int i = 1; i < currentMax + 2; i++) {
				if (i == currentMax + 1) {
					if (!isWinning(n - i, currentMax + 1)) {
						lose = 1;
					}
				} else {
					if (!isWinning(n - i, currentMax)) {
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
		}

		void printSpace() {
			map<pii, bool>::iterator it;
			for(it = mem.begin(); it != mem.end(); it++) {
				cout<<((*it).first.first)<<" "<<((*it).first.second)<<" "<<((*it).second ? "Win" : "Lose")<<endl;
			}
		}

		int calculateNextMove() {

		}
};

int main() {
	int n;
	cin>> n;

	ExpandingNim *obj = new ExpandingNim(n);

	obj->printSpace();

	return 0;
}
