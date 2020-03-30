package io.github.frc5024.libfms.model;

public class Team {

    private int teamNum;

    /**
     * Create a team
     * 
     * @param number FRC team number
     */
    public Team(int number) {
        teamNum = number;
    }

    /**
     * Get team's number
     * 
     * @return Team number
     */
    public int getTeamNumber() {
        return teamNum;
    }

    /**
     * Get team's name
     * 
     * @return Team name
     */
    public String getTeamName() {
        return "Unnamed Team";
    }
}