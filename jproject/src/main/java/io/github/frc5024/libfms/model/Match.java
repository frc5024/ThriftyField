package io.github.frc5024.libfms.model;

/**
 * Model class for an FRC match
 */
public class Match {

    /**
     * Mapping of competition level to FMS int
     */
    public enum CompetitionLevel {
        TEST(0), PRACTICE(1), QUALIFICATION(2), ELIMINATION(3);

        protected int f;

        private CompetitionLevel(int f) {
            this.f = f;
        }
    }

    /* Match info */
    private int number;
    private int replay;
    private CompetitionLevel level;

    /**
     * Create an FRC match
     * 
     * @param number Match number
     * @param level  Competition level
     */
    public Match(int number, CompetitionLevel level) {
        this(number, 0, level);
    }

    /**
     * Create an FRC match
     * 
     * @param number Match number
     * @param replay Replay number
     * @param level  Competition level
     */
    public Match(int number, int replay, CompetitionLevel level) {
        this.number = number;
        this.replay = replay;
        this.level = level;
    }

    /**
     * Get the match number
     * 
     * @return Match number
     */
    public int getMatchNumber() {
        return number;
    }

    /**
     * Get the replay number
     * 
     * @return Replay number
     */
    public int getReplayNumber() {
        return replay;
    }

    /**
     * Get the competition level
     * 
     * @return Level
     */
    public CompetitionLevel getLevel() {
        return level;
    }

    /**
     * Get the FMS-formatted competition level int
     * 
     * @return Level int
     */
    public int getLevelCode() {
        return level.f;
    }

}