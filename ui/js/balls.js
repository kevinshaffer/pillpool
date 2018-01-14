/* Ball handling functions */
function ballClick(_ball){
    var _current_state = _ball.data().state;
    if (_current_state === "live"){
        console.log('potBall');
        potBall(_ball);
    }
    else {
        console.log('unPot Ball');
        unPotBall(_ball);
    }
};

function potBall(_ball){
    _ball.fadeTo(50, .25);
    _ball.data().state = "potted";
}

function unPotBall(_ball){
    _ball.fadeTo(50, 1);
    _ball.data().state = "live";
}
