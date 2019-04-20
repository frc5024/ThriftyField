var modifier = 1;
var alliance = "red"

function setScore(score) {
    console.log('/api/score/' + alliance + "/" + score * modifier);
    $.getJSON('/api/score/' + alliance + "/" + score * modifier, function (data) {
        console.log(data);
      });
}

function setMode(mode) {
    if (mode == "-"){
        modifier = -1
    } else {
        modifier = 1
    }
}

var urlParams = new URLSearchParams(window.location.search);
var _alliance = urlParams.get("alliance");
if (_alliance) {
    if (_alliance == "blue") {
        alliance = _alliance
    }
}