package io.github.frc5024.libfms.driverstation;

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
         * @return Flag
         */
        public int getFlag() {
            return flag;
        }

        /**
         * Combine multiple RobotStates together into one flag
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

    public enum AllianceStationID {

    }

}