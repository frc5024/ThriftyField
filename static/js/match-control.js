var lowBatteryThreshold = 8;

function startMatch() {
    console.log("Starting match")
    $.getJSON('/api/'+api_key+'/control/startmatch', function (data) {
        console.log(data);
      });
}

function stopMatch() {
    $.getJSON('/api/'+api_key+'/control/stopmatch', function (data) {
        console.log(data);
      });
}

function substituteTeam(team, station) {
    $.getJSON('/api/'+api_key+'/control/alliancestation/' + station + '/' + team, function (data) {
        console.log(data);
      });
}

function toggleBypass(station) {
    $.getJSON('/api/'+api_key+'/control/bypass/' + station, function (data) {
        console.log(data);
      });
}

var handleArenaStatus = function (data) {
  
    // Update the team status view.
    $.each(data.AllianceStations, function(station, stationStatus) {
  
      if (stationStatus.driverstation_connection) {
        // Format the driver station status box.
        var dsConn = stationStatus.driverstation_connection;
          $("#status" + station + " .ds-status").attr("data-status-ok", dsConn.ds_linked);
  
        // Format the robot status box.
        var robotOkay = dsConn.battery_voltage > lowBatteryThreshold && dsConn.robot_linked;
        $("#status" + station + " .robot-status").attr("data-status-ok", robotOkay);
        if (stationStatus.DsConn.seconds_since_last_robot_link > 1 && stationStatus.DsConn.seconds_since_last_robot_link < 1000) {
          $("#status" + station + " .robot-status").text(stationStatus.DsConn.seconds_since_last_robot_link.toFixed());
        } else {
          $("#status" + station + " .robot-status").text(dsConn.battery_voltage.toFixed(1) + "V");
        }
      } else {
        $("#status" + station + " .ds-status").attr("data-status-ok", "");
        $("#status" + station + " .robot-status").attr("data-status-ok", "");
        $("#status" + station + " .robot-status").text("");
  
        // Format the robot status box according to whether the AP is configured with the correct SSID.
        // var expectedTeamId = stationStatus.Team ? stationStatus.Team.Id : 0;
        // if (wifiStatus.TeamId === expectedTeamId) {
        //   if (wifiStatus.RadioLinked) {
        //     $("#status" + station + " .radio-status").attr("data-status-ok", true);
        //   } else {
        //     $("#status" + station + " .radio-status").attr("data-status-ok", "");
        //   }
        // } else {
        //   $("#status" + station + " .radio-status").attr("data-status-ok", false);
        // }
      }
  
      if (stationStatus.estop) {
        $("#status" + station + " .bypass-status").attr("data-status-ok", false);
        $("#status" + station + " .bypass-status").text("ES");
      } else if (stationStatus.bypass) {
        $("#status" + station + " .bypass-status").attr("data-status-ok", false);
        $("#status" + station + " .bypass-status").text("B");
      } else {
        $("#status" + station + " .bypass-status").attr("data-status-ok", true);
        $("#status" + station + " .bypass-status").text("");
      }
    });
  
    // Enable/disable the buttons based on the current match state.
    // switch (matchStates[data.MatchState]) {
    //   case 0: //pre match
    //     $("#startMatch").prop("disabled", !data.CanStartMatch);
    //     $("#abortMatch").prop("disabled", true);
    //     break;
    //   case "START_MATCH":
    //   case "AUTO_PERIOD":
    //   case "PAUSE_PERIOD":
    //   case "TELEOP_PERIOD":
    //   case "ENDGAME_PERIOD":
    //     $("#startMatch").prop("disabled", true);
    //     $("#abortMatch").prop("disabled", false);
    //     $("#commitResults").prop("disabled", true);
    //     $("#discardResults").prop("disabled", true);
    //     $("#editResults").prop("disabled", true);
    //     $("#startTimeout").prop("disabled", true);
    //     break;
    //   case "POST_MATCH":
    //     $("#startMatch").prop("disabled", true);
    //     $("#abortMatch").prop("disabled", true);
    //     $("#commitResults").prop("disabled", false);
    //     $("#discardResults").prop("disabled", false);
    //     $("#editResults").prop("disabled", false);
    //     $("#startTimeout").prop("disabled", true);
    //     break;
    //   case "TIMEOUT_ACTIVE":
    //     $("#startMatch").prop("disabled", true);
    //     $("#abortMatch").prop("disabled", false);
    //     $("#commitResults").prop("disabled", true);
    //     $("#discardResults").prop("disabled", true);
    //     $("#editResults").prop("disabled", true);
    //     $("#startTimeout").prop("disabled", true);
    //     break;
    //   case "POST_TIMEOUT":
    //     $("#startMatch").prop("disabled", true);
    //     $("#abortMatch").prop("disabled", true);
    //     $("#commitResults").prop("disabled", true);
    //     $("#discardResults").prop("disabled", true);
    //     $("#editResults").prop("disabled", true);
    //     $("#startTimeout").prop("disabled", true);
    //     break;
    // }
  
    // if (data.PlcIsHealthy) {
    //   $("#plcStatus").text("Connected");
    //   $("#plcStatus").attr("data-ready", true);
    // } else {
    //   $("#plcStatus").text("Not Connected");
    //   $("#plcStatus").attr("data-ready", false);
    // }
    // $("#fieldEstop").attr("data-ready", !data.FieldEstop);
  
    // if (matchStates[data.MatchState] !== "PRE_MATCH") {
    //   $("#gameSpecificData").val(data.GameSpecificData);
    // }
  };

function sleep(ms) {
    var start = new Date().getTime(), expire = start + ms;
    while (new Date().getTime() < expire) { }
    return;
}

function update() {
    $.getJSON('/api/fieldinfo', function (data) {
        // console.log(data);
        handleArenaStatus(data);
        sleep(1000)
        update() 
    });
}



update();