<?php
//ini_set('display_errors', 'On');
//ini_set('display_startup_errors', true);
//error_reporting(E_ALL);
include "GameController.php";
include "Board.php";
$myController = new GameController("localhost",$argv[1]);
$myGame = new Board(25,15,3);
$myController->createConnection();

while(!$myGame->gameOver){
    echo "--------------------------------------------------------------------------------------------------------------\n";
    $sendingString = $myGame->generateSendingString();
    if($sendingString[0] == '1'){
        echo "Placing Stage, board state: \n";
    } else {
        echo "Removing Stage, board state: \n";
    }
    echo substr($sendingString, 2 , strlen($sendingString) - 4)."\n";
    $myController->send($myGame->currentTurn, $myGame->generateSendingString());
    $time1 = microtime();
    $move = $myController->recv($myGame->currentTurn);
    $time2 = microtime();
    $myGame->updateTime($myGame->currentTurn, $time2 - $time1);
    $myMove = explode(" ", $move);
    if($myGame->currentState == "place") {
        $myGame->move((int)$myMove[0], (int)$myMove[1]);
    }
    else {
        $myGame->remove((int)$myMove[0]);
    }
}
$myController->send(1, $myGame->generateSendingString());
$myController->send(2, $myGame->generateSendingString());
$myController->closeConnection();
