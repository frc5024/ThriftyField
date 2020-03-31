package io.github.frc5024.libfms.driverstation;

import io.github.frc5024.libfms.model.Match;

/**
 * Driverstation control packet.
 * 
 * Note to anyone working here: You will want a good understanding of bitmasks
 * and binary.
 */
public class ControlPacket {

    /**
     * Robot control state
     */
    public enum RobotState {
        DISABLED(0x00), // Robot disabled
        AUTONOMOUS(0x02), // Autonomous active
        ENABLED(0x04), // Robot enabled
        ESTOPPED(0x80); // Robot estopped

        private int flag;

        private RobotState(int flag) {
            this.flag = flag;
        }

        /**
         * Get the RobotState as an integer flag
         * 
         * @return Flag
         */
        public int getFlag() {
            return flag;
        }

        /**
         * Combine multiple RobotStates together into one flag
         * 
         * @param states States
         * @return Flag
         */
        public static int buildFlag(RobotState... states) {
            int flag = 0x00;
            for (RobotState state : states) {
                flag |= state.getFlag();
            }
            return flag;
        }
    }

    /**
     * Mapping from alliance station to FMS int
     */
    public enum AllianceStationID {
        RED1(0x00), RED2(0x01), RED3(0x02), BLUE1(0x03), BLUE2(0x04), BLUE3(0x05);

        private int id;

        private AllianceStationID(int id) {
            this.id = id;
        }

        /**
         * Get the AllianceStationID int
         * 
         * @return ID
         */
        public int getID() {
            return id;
        }

    }

    /* Packet data */
    private int robotFlag;
    private Match match;
    private long unixTime;
    private int matchSeconds;

    /**
     * Build a control packet to send to DriverStation.
     * 
     * @param robotStateFlag The flag for robot state. Should be built with
     *                       {@link RobotState}.buildFlag()
     * @param match          Current match
     * @param unixTime       FMS system unix timestamp
     * @param matchSeconds   Number of seconds remaining in the match
     */
    public ControlPacket(int robotStateFlag, Match match, long unixTime, int matchSeconds) {
        this.robotFlag = robotStateFlag;
        this.match = match;
        this.unixTime = unixTime;
        this.matchSeconds = matchSeconds;
    }

    public byte[] encode(AllianceStationID station, int dsPacketCount) {

        return null;
    }

}