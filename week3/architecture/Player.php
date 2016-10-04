<?php
class Player
{
    public $WeightState;
    public $timeLeft;

    function __construct($numberOfWeight){
        for($i = 1; $i <= $numberOfWeight; $i++){
            $this->WeightState[$i] = true;
        }
        $this->timeLeft = 120.0;
    }
}