// Copyright 2018 Team 254. All Rights Reserved.
// Author: pat@patfairbank.com (Patrick Fairbank)
//
// Client-side logic for the field monitor display.

var websocket;
var redSide;
var blueSide;
var lowBatteryThreshold = 8;

// Handles a websocket message to update the team connection status.
var handleArenaStatus = function (data) {
  $.each(data.AllianceStations, function(station, stationStatus) {
    // Select the DOM elements corresponding to the team station.
    var teamElementPrefix;
    if (station[0] === "R") {
      teamElementPrefix = "#" + redSide + station[1];
    } else {
      teamElementPrefix = "#" + blueSide  + station[1];
    }
    var teamIdElement = $(teamElementPrefix + "-ID");
    var teamDsElement = $(teamElementPrefix + "-DS");
    var teamRadioElement = $(teamElementPrefix + "-Radio");
    var teamRadioTextElement = $(teamElementPrefix + "-Radio span");
    var teamRobotElement = $(teamElementPrefix + "-Robot");
    var teamBypassElement = $(teamElementPrefix + "-Bypass");

    var redScore = document.getElementById("rscore");
    var blueScore = document.getElementById("bscore");
    var timer = document.getElementById("time");

    redScore.innerHTML = data.scores.red;
    blueScore.innerHTML = data.scores.blue;
    timer.innerHTML = data.time;


    
    if (stationStatus.team) {
      // Set the team number and status.
      teamIdElement.text(stationStatus.team.id);
      var status = "no-link";
      if (stationStatus.bypass) {
        status = "";
      } else if (stationStatus.driverstation_connection) {
        if (stationStatus.driverstation_connection.robot_linked) {
          status = "robot-linked";
        } else if (stationStatus.driverstation_connection.radio_linked) {
          status = "radio-linked";
        } else if (stationStatus.driverstation_connection.ds_linked) {
          status = "ds-linked";
        }
      }
      teamIdElement.attr("data-status", status);
    } else {
      // No team is present in this position for this match; blank out the status.
      teamIdElement.text("");
      teamIdElement.attr("data-status", "");
    }


    if (stationStatus.driverstation_connection) {
      // Format the driver station status box.
      var driverstation_connection = stationStatus.driverstation_connection;
      teamDsElement.attr("data-status-ok", driverstation_connection.ds_linked);

      // Format the radio status box according to the connection status of the robot radio.
      // var radioOkay = stationStatus.Team && stationStatus.Team.Id === wifiStatus.TeamId && wifiStatus.RadioLinked;
      // teamRadioElement.attr("data-status-ok", radioOkay);

      // Format the robot status box.
      var robotOkay = driverstation_connection.battery_voltage > lowBatteryThreshold && driverstation_connection.robot_linked;
      teamRobotElement.attr("data-status-ok", robotOkay);
      if (stationStatus.driverstation_connection.seconds_since_last_robot_link > 1 && stationStatus.driverstation_connection.seconds_since_last_robot_link < 1000) {
        teamRobotElement.text(stationStatus.driverstation_connection.seconds_since_last_robot_link.toFixed());
      } else {
        teamRobotElement.text(driverstation_connection.battery_voltage.toFixed(1) + "V");
      }
    } else {
      teamDsElement.attr("data-status-ok", "");
      teamRobotElement.attr("data-status-ok", "");
      teamRobotElement.text("RBT");

      // Format the robot status box according to whether the AP is configured with the correct SSID.
      // var expectedTeamId = stationStatus.Team ? stationStatus.Team.Id : 0;
      // if (wifiStatus.TeamId === expectedTeamId) {
      //   if (wifiStatus.RadioLinked) {
      //     teamRadioElement.attr("data-status-ok", true);
      //   } else {
      //     teamRadioElement.attr("data-status-ok", "");
      //   }
      // } else {
      //   teamRadioElement.attr("data-status-ok", false);
      // }
    }

    if (stationStatus.estop) {
      teamBypassElement.attr("data-status-ok", false);
      teamBypassElement.text("ES");
    } else if (stationStatus.bypass) {
      teamBypassElement.attr("data-status-ok", false);
      teamBypassElement.text("BYP");
    } else {
      teamBypassElement.attr("data-status-ok", true);
      teamBypassElement.text("ES");
    }
  });
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

$(function() {
  // Read the configuration for this display from the URL query string.
  var urlParams = new URLSearchParams(window.location.search);
  var reversed = urlParams.get("reversed");
  if (reversed === "true") {
    redSide = "R";
    blueSide = "B";
  } else {
    redSide = "R";
    blueSide = "B";
  }
  $(".reversible-left").attr("data-reversed", reversed);
  $(".reversible-right").attr("data-reversed", reversed);

  // Set up the websocket back to the server.
  // websocket = new CheesyWebsocket("/displays/field_monitor/websocket", {
  //   arenaStatus: function(event) { handleArenaStatus(event.data); }
  // });

  console.log("Listening to field");
  update(); // Recursive function
});
