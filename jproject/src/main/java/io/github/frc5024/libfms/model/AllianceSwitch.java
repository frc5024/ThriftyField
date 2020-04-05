package io.github.frc5024.libfms.model;

import ca.retrylife.ewmath.MathUtils;
import io.github.frc5024.libfms.AllianceStation;
import io.github.frc5024.libfms.driverstation.ControlPacket.AllianceStationID;

/**
 * Hub for teams on an alliance
 */
public class AllianceSwitch {

    // Red alliance
    private static AllianceSwitch redAlliance;

    // Blue alliance
    private static AllianceSwitch blueAlliance;

    // List of all stations to be connected
    private AllianceStation[] stations;

    private AllianceSwitch(AllianceStation station1, AllianceStation station2, AllianceStation station3) {

        // Build station list
        stations = new AllianceStation[3];
        stations[0] = station1;
        stations[1] = station2;
        stations[2] = station3;
    }

    /**
     * Get the red alliance
     * 
     * @return Red alliance
     */
    public static AllianceSwitch getRedAlliance() {
        if (redAlliance == null) {
            // Configure the entire alliance
            redAlliance = new AllianceSwitch(new AllianceStation(AllianceStationID.RED1),
                    new AllianceStation(AllianceStationID.RED2), new AllianceStation(AllianceStationID.RED3));
        }
        return redAlliance;
    }

    /**
     * Get the blue alliance
     * 
     * @return Blue alliance
     */
    public static AllianceSwitch getBlueAlliance() {
        if (blueAlliance == null) {
            // Configure the entire alliance
            blueAlliance = new AllianceSwitch(new AllianceStation(AllianceStationID.BLUE1),
                    new AllianceStation(AllianceStationID.BLUE2), new AllianceStation(AllianceStationID.BLUE3));
        }
        return blueAlliance;
    }

    /**
     * Get station 1
     * 
     * @return Station 1
     */
    public AllianceStation getStation1() {
        return stations[0];
    }

    /**
     * Get station 2
     * 
     * @return Station 2
     */
    public AllianceStation getStation2() {
        return stations[1];
    }

    /**
     * Get station 3
     * 
     * @return Station 3
     */
    public AllianceStation getStation3() {
        return stations[2];
    }

    /**
     * Get an ordered list of all alliance stations
     * 
     * @return All stations
     */
    public AllianceStation[] getAllStations() {
        return stations;
    }
}