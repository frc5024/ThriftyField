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

    /**
     * Encode this ControlPacket into UDP data to be sent to DriverStation
     * 
     * @param station       Alliance station ID
     * @param dsPacketCount Packet counter value from DriverStation connection
     * @return Encoded packet
     */
    public byte[] encode(AllianceStationID station, int dsPacketCount) {
        // This encoding is as defined at:
        // https://frcture.readthedocs.io/en/latest/driverstation/fms_to_ds.html

        // Build an output buffer
        byte[] output = new byte[22];

        // Encode packet number
        output[0] = (byte) ((dsPacketCount >> 8) & 0xff);
        output[1] = (byte) (dsPacketCount & 0xff);

        // Encode the protocol version
        output[2] = (byte) 0x00;

        // Encode robot status flag
        output[3] = (byte) robotFlag;

        // Encode request byte
        // (Nobody seems to know what this is used for)
        output[4] = (byte) 0x00;

        // Encode the alliance station ID
        output[5] = (byte) station.getID();

        // Encode the match type
        output[6] = (byte) match.getLevelCode();

        // Encode the match number
        output[7] = (byte) ((dsPacketCount >> 8) & 0xff);
        output[8] = (byte) (dsPacketCount & 0xff);

        // Encode the play number
        output[9] = (byte) (1 + match.getReplayNumber());

        // Determine microseconds and seconds from unixtime
        long unixMicros = unixTime * 1000;
        unixTime /= 1000;

        // Encode the system time in microseconds
        output[10] = (byte) ((unixMicros >> 24) & 0xff);
        output[11] = (byte) ((unixMicros >> 16) & 0xff);
        output[12] = (byte) ((unixMicros >> 8) & 0xff);
        output[13] = (byte) (unixMicros & 0xff);

        // Encode the date and time
        output[14] = (byte) (unixTime % 60);
        output[15] = (byte) ((unixTime / 60) % 60);
        output[16] = (byte) ((unixTime / 3600) % 24);
        // Now.. Since this isn't mission critical, I think it is safe to just hardcode
        // 30 days per month? As far as I know, this info is only used for DS logs.
        output[17] = (byte) ((unixTime / 604800) % 30);
        output[18] = (byte) ((unixTime / 2629743) % 12);
        output[19] = (byte) ((unixTime / 31556926) - 1900);

        // Encode remaining time in the match
        output[20] = (byte) ((matchSeconds >> 8) & 0xff);
        output[21] = (byte) (matchSeconds & 0xff);

        return output;
    }

}