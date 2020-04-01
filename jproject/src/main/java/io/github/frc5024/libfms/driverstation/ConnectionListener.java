package io.github.frc5024.libfms.driverstation;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Arrays;

import io.github.frc5024.libfms.AllianceStation;
import io.github.frc5024.libfms.driverstation.ControlPacket.AllianceStationID;
import io.github.frc5024.libfms.model.AllianceSwitch;
import io.github.frc5024.libfms.model.Team;
import io.github.frc5024.libfms.scheduling.MatchSchedule;
import io.github.frc5024.util.Logger;

/**
 * Service that listens for DriverStations looking to connect to the field. This
 * acts as a bit of a dispatcher, and will tell teams where they are assigned,
 * or drop them if not playing this match.
 */
public class ConnectionListener extends Thread {

    // Driverstation listener socket
    private ServerSocket socket;

    // Tracker for listening
    private boolean shouldAccept = true;

    public ConnectionListener() throws IOException {

        Logger.log("ConnectionListener", "Listening for DriverStations looking to connect to the field.");
        socket = new ServerSocket(1750);
        Logger.log("ConnectionListener", "Opened listener socket on port 1750");
        Logger.log("ConnectionListener",
                "If this device is not assigned ip 10.0.100.5, DriverStations cannot connect!");

    }

    @Override
    public void run() {

        Logger.log("ConnectionListener", "Listening for DriverStations");

        while (true) {
            try {
                // Accept connection
                Socket connection = socket.accept();
                String hostAddr = connection.getInetAddress().getHostAddress();

                // Drop the connection if the field is not currently accepting DS connections
                if (!shouldAccept) {
                    Logger.log("ConnectionListener",
                            String.format("Dropping connection from %s because shouldAccept is false", hostAddr));
                    connection.close();
                    continue;
                }

                // Read request info
                byte[] data = new byte[5];
                DataOutputStream output = new DataOutputStream(new BufferedOutputStream(connection.getOutputStream()));
                DataInputStream input = new DataInputStream(new BufferedInputStream(connection.getInputStream()));
                while (input.read(data) > 0) {
                }

                // Require data to be sent
                if (data.equals(new byte[5])) {
                    Logger.log("ConnectionListener", String.format("%s send no data. Dropping connection", hostAddr));
                    connection.close();
                    continue;
                }

                // Require the correct data format
                if (!(data[0] == (byte) 0x00 && data[1] == (byte) 0x03 && data[2] == (byte) 0x18)) {
                    Logger.log("ConnectionListener",
                            String.format("%s sent invalid data: %s", hostAddr, Arrays.toString(data)));
                    connection.close();
                    continue;
                }

                // Parse out the team number
                int teamNumber = data[3] << 8 | data[4];

                // Log the mapping between IP and team number
                Logger.log("ConnectionListener", String.format("%s is team %d", hostAddr, teamNumber));

                // Find the assigned alliance station for this team
                AllianceStationID station = MatchSchedule.getInstance().getCurrentTeamsList()
                        .getStationIDForTeam(teamNumber);

                // Reject the connection if the team is not supposed to be fielded
                if (station == null) {
                    Logger.log("ConnectionListener", String.format(
                            "Rejecting connection from team %d, who is not supposed to be on the field", teamNumber));
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                    }
                    connection.close();
                    continue;
                }

                // ThriftyField is not set up to work with the real FMS switches, so we cannot
                // determine a team's current station based on their subnet. All we can do is
                // say "ya, sure. you are in the right spot". We shall rely on the event staff
                // or team members to put themselves in the correct station.
                boolean isInCorrectStation = true;

                // Build a response packet
                byte[] response = new byte[5];

                // FMS message type header
                response[0] = (byte) 0x00;
                response[1] = (byte) 0x03;
                response[2] = (byte) 0x19;

                // Assigned station ID
                response[3] = (byte) station.getID();

                // Is in correct station?
                response[4] = (byte) ((isInCorrectStation) ? 0 : 1);

                // Log the assignment
                Logger.log("ConnectionListener", String.format("Accepting connection from team %d in station %s",
                        teamNumber, station.toString()));

                // Respond with this data
                output.write(response);

                // Configure the newly assigned alliance station
                AllianceStation stationController = null;
                switch (station) {
                    case BLUE1:
                        stationController = AllianceSwitch.getBlueAlliance().getStation1();
                        break;
                    case BLUE2:
                        stationController = AllianceSwitch.getBlueAlliance().getStation2();
                        break;
                    case BLUE3:
                        stationController = AllianceSwitch.getBlueAlliance().getStation3();
                        break;
                    case RED1:
                        stationController = AllianceSwitch.getRedAlliance().getStation1();
                        break;
                    case RED2:
                        stationController = AllianceSwitch.getRedAlliance().getStation2();
                        break;
                    case RED3:
                        stationController = AllianceSwitch.getRedAlliance().getStation3();
                        break;
                    default:
                        Logger.log("ConnectionListener",
                                "Something went very wrong. An invalid alliance station made it past edge checks!");
                        break;
                }

                // Configure the station team
                stationController.setTeam(new Team(teamNumber));

                // Set up the DriverStation connection
                stationController.connectDriverStation(hostAddr);

            } catch (IOException e) {
                Logger.log("ConnectionListener", "Exception thrown. Dropping connection");
                e.printStackTrace();
            }
        }

    }

    /**
     * Set if the listener should be allowing DriverStations to connect
     * 
     * @param accept Should allow?
     */
    public void acceptDSConnections(boolean accept) {
        shouldAccept = accept;
    }

}