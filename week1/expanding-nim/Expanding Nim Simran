#include <iostream>

using namespace std;

int WinningStateMap[40][200];
int myMove[2] ;

void initStateMap();
void makeMove(int,int);
void findWinningStates(int,int);
void printMap(int) ;

int PebblesMax = 0;

int main()
{
   int pickPebbles, Cmax = 2, pebblesLeft ;
   initStateMap();
   cout << "Enter number of pebbles in heap" <<endl ;
   cin >> PebblesMax ;
   cout << "Enter Current Max" <<endl ;
   cin >> Cmax ;
   pebblesLeft = PebblesMax ;
   makeMove(PebblesMax, Cmax);
   while(true) {
        pickPebbles = myMove[0] ;
        pebblesLeft = pebblesLeft - pickPebbles ;
        if(pebblesLeft <=0) {
            break;
        }
        Cmax = myMove[1] ;
        cout << "Pebbles picked: " << pickPebbles << "  Pebbles left: " << pebblesLeft << "  Current Max: " << Cmax << endl ;
        cout << "Enter Amout of pebbles you want to pick:" ;
        cin >> pickPebbles ;
        pebblesLeft = pebblesLeft - pickPebbles ;
        if(pickPebbles == (Cmax +1) ) {
           Cmax++;
        }
        if(pebblesLeft<=0) {
            break;
        }
        makeMove(pebblesLeft, Cmax);
    } 
    //printMap(Cmax) ;
    cout << "finishing" <<endl ;
   return 0;
}

void initStateMap(){
    for (int i=2;i<=40;i++){
        for(int j=1;j<=200;j++){
            if(j<=(i+1)) {
                WinningStateMap[i][j] = 1 ;
            } else if(j==(i+2)) {
                WinningStateMap[i][j] = 0 ;
            } else {
                WinningStateMap[i][j] = -1 ;
            }
        }
    }
}

void makeMove(int n,int Cmax){
    //if n is less than or equal to Cmax + 1 the take away n pebbles
    if(n<=(Cmax+1)) {
        myMove[0] = n ;
        myMove[1] = (n < Cmax) ? Cmax : n;
        return ;
    }
    
    for(int i=1;i<=Cmax;i++){
        if(WinningStateMap[Cmax][n-i] == -1){
            findWinningStates(n-i,Cmax);
        }
        //after making move next state should be loosing state
        if(WinningStateMap[Cmax][n-i] == 0){
            myMove[0] = i ;
            myMove[1] = Cmax ;
            return ;
        }
    }
    
    //increasing Current Max
    if(WinningStateMap[Cmax+1][n-Cmax-1] == -1){
        findWinningStates(n-Cmax-1,Cmax+1);
    }
    if(WinningStateMap[Cmax+1][n-Cmax-1] == 0){
        myMove[0] = Cmax+1 ;
        myMove[1] = Cmax+1 ;
        return ;
    }
    if(WinningStateMap[Cmax+1][n-Cmax-1] == 1){
        myMove[0] = Cmax+1 ;
        myMove[1] = Cmax+1 ;
        cout<< "Already Lost" << endl ;
        return ;
    }
    
}

void findWinningStates(int n,int Cmax){
    
    //this would be winning state if at least one state from this state is loosing state
    for(int i=1;i<=Cmax;i++) {
        if(WinningStateMap[Cmax][n-i] == -1){
            findWinningStates(n-i,Cmax);
        }
        
        if(WinningStateMap[Cmax][n-i] == 0){
            WinningStateMap[Cmax][n] = 1;
            return ;
        }
    }
    
    //this is loosing state if all possible states from this state are winning states   
    //increasing Current Max
    if(WinningStateMap[Cmax+1][n-Cmax-1] == -1){
        findWinningStates(n-Cmax-1,Cmax+1);
    }
    if(WinningStateMap[Cmax+1][n-Cmax-1] == 0){
        WinningStateMap[Cmax][n] = 1;
        return;
    } else {
        WinningStateMap[Cmax][n] = 0;
    }
    
}

void printMap(int Cmax) {
    for (int i= 2 ; i<=10; i++) {
        cout << i <<": " ;
        for(int j=1; j<= 40; j++) {
            cout << WinningStateMap[i][j] << " " ;
        }
        cout<< endl ;
    }
}
