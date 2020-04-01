package io.github.frc5024.libfms.scheduling;

public class MatchSchedule {
    private static MatchSchedule instance;

    private MatchSchedule(){  

    }
    
    public static MatchSchedule getInstance() {
        if (instance == null) {
            instance = new MatchSchedule();
        }
        return instance;
    }

    public void getCurrentTeamsList() {
        
    }
    
}