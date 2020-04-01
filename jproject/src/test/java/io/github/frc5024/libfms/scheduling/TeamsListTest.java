package io.github.frc5024.libfms.scheduling;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

import io.github.frc5024.libfms.driverstation.ControlPacket.AllianceStationID;
import io.github.frc5024.libfms.model.Team;

public class TeamsListTest {

    private TeamsList teams = new TeamsList(new Team(1), new Team(2), new Team(3), new Team(4), new Team(5),
            new Team(6));

            @Test
            public void testRedTeamFinding() {

                // Check for valid teams
                assertTrue("Red1 is team 1", teams.getStationIDForTeam(1).equals(AllianceStationID.RED1));
                assertTrue("Red2 is team 2", teams.getStationIDForTeam(2).equals(AllianceStationID.RED2));
                assertTrue("Red3 is team 3", teams.getStationIDForTeam(3).equals(AllianceStationID.RED3));

                // Check for an invalid team
                assertTrue("Team 5024 is not playing", teams.getStationIDForTeam(5024) == null);

            }
            
            @Test
    public void testBlueTeamFinding() {

        // Check for valid teams
        assertTrue("Blue1 is team 4", teams.getStationIDForTeam(4).equals(AllianceStationID.BLUE1));
        assertTrue("Blue2 is team 5", teams.getStationIDForTeam(5).equals(AllianceStationID.BLUE2));
        assertTrue("Blue3 is team 6", teams.getStationIDForTeam(6).equals(AllianceStationID.BLUE3));

        // Check for an invalid team
        assertTrue("Team 5024 is not playing", teams.getStationIDForTeam(5024) == null);

    }


}