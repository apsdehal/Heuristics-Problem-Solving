#include <iostream>
#include "custom_socket.h"

using namespace std;

//We will ignore array index with 0 
const int MAX_POINTS = 1001 ;
int pull[MAX_POINTS][MAX_POINTS];
int maxStones = 0;
tcp_client c;
int socketNo = 9000;

void initPull();
string * getTokens();

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

	//putting in infinite loop till server signals that game has ended
	while(true){
		data = getTokens();
		//check if game has ended
		if (stoi(data[0]) == 1){
			break;
		}
		//game logic
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
	for (int i = 1; i < MAX_POINTS; i++)
	{
		for (int j = 1; j < MAX_POINTS; j++)
		{
			pull[i][j] = 0;
		}
	}
}