var modifier = 1;
var alliance = "red"

function setScore(score) {
    $.getJSON('/api/'+api_key+'/score/' + alliance + "/" + score * modifier, function (data) {
        console.log(data);
      });
}

function setMode(mode) {
    if (mode == "-"){
        modifier = -1;
    } else {
        modifier = 1;
    }

    var elements = document.getElementsByClassName('num');
    for (var i in elements) {
        if (modifier == -1) {
            elements[i].className = "btn btn-sm btn-danger btn-referee num"           
        } else {
            elements[i].className = "btn btn-sm btn-success btn-referee num"
        }
    }
}

var urlParams = new URLSearchParams(window.location.search);
var _alliance = urlParams.get("alliance");
if (_alliance) {
    if (_alliance == "blue") {
        alliance = _alliance
    }
}