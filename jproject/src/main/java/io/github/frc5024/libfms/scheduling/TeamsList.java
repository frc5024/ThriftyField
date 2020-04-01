package io.github.frc5024.libfms.scheduling;

import io.github.frc5024.libfms.driverstation.ControlPacket.AllianceStationID;
import io.github.frc5024.libfms.model.Team;

/**
 * A list of all teams for a match
 */
public class TeamsList {

    /* Alliances */
    private Team[] redAlliance = new Team[3];
    private Team[] blueAlliance = new Team[3];

    /**
     * Build a TeamsList
     * 
     * @param red1  Red team 1
     * @param red2  Red team 2
     * @param red3  Red team 3
     * @param blue1 Blue team 1
     * @param blue2 Blue team 2
     * @param blue3 Blue team 3
     */
    public TeamsList(Team red1, Team red2, Team red3, Team blue1, Team blue2, Team blue3) {

        // Set up the Red alliance
        redAlliance[0] = red1;
        redAlliance[1] = red2;
        redAlliance[2] = red3;

        // Set up blue alliance
        blueAlliance[0] = blue1;
        blueAlliance[1] = blue2;
        blueAlliance[2] = blue3;
    }

    /**
     * Find the appropriate alliance station for a team. Null if not fielded
     * 
     * @param number Team number
     * @return AllianceStationID
     */
    public AllianceStationID getStationIDForTeam(int number) {

        int position = -1;
        int alliance = -1;

        // Finder code for checking team position
        positionFinder: {

            // Search Red alliance for team
            for (int i = 0; i < redAlliance.length; i++) {
                if (redAlliance[i].getTeamNumber() == number) {

                    // Set the position info
                    alliance = 0;
                    position = i + 1;

                    // Break out of position finding
                    break positionFinder;

                }
            }

            // Search Blue alliance for team
            for (int i = 0; i < blueAlliance.length; i++) {
                if (blueAlliance[i].getTeamNumber() == number) {

                    // Set the position info
                    alliance = 10;
                    position = i + 1;

                    // Break out of position finding
                    break positionFinder;

                }
            }

        }

        // If there is no position, this team is not to be fielded
        if (position == -1) {
            return null;
        }

        // Build and return the AllianceStationID
        switch (position + alliance) {
            case 1:
                return AllianceStationID.RED1;
            case 2:
                return AllianceStationID.RED2;
            case 3:
                return AllianceStationID.RED3;
            case 10:
                return AllianceStationID.BLUE1;
            case 12:
                return AllianceStationID.BLUE2;
            case 13:
                return AllianceStationID.BLUE3;
            default:
                return null;
        }

    }

}