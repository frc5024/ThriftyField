function startMatch() {
    console.log("Starting match")
    $.getJSON('/api/control/startmatch', function (data) {
        console.log(data);
      });
}

function stopMatch() {
    $.getJSON('/api/control/stopmatch', function (data) {
        console.log(data);
      });
}

function substituteTeam(team, station) {
    $.getJSON('/api/control/alliancestation/' + station + '/' + team, function (data) {
        console.log(data);
      });
}