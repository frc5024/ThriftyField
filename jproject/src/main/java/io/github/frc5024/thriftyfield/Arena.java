package io.github.frc5024.thriftyfield;

import java.io.IOException;

import io.github.frc5024.libfms.AllianceStation;
import io.github.frc5024.libfms.driverstation.ConnectionListener;
import io.github.frc5024.libfms.driverstation.ControlPacket;
import io.github.frc5024.libfms.model.AllianceSwitch;
import io.github.frc5024.thriftyfield.gameplay.GameStateManager;
import io.github.frc5024.util.Logger;

/**
 * The arena contains everything on the field
 */
public class Arena implements Runnable {
    private static Arena instance;

    // Driverstation connection listener
    private ConnectionListener dsConnectionListener;

    // Alliances
    private AllianceSwitch redAlliance;
    private AllianceSwitch blueAlliance;

    // Game logic
    private GameStateManager gameStateManager;

    private Arena() {

        // Set up the driverstation listener
        try {
            dsConnectionListener = new ConnectionListener();
            Logger.log("Arena", "Now listening for DriverStations");
        } catch (IOException e) {
            Logger.log("Arena", "Failed to start driverstation listener!");
            e.printStackTrace();
            System.exit(1);
        }

        // Set up both alliances
        redAlliance = AllianceSwitch.getRedAlliance();
        blueAlliance = AllianceSwitch.getBlueAlliance();

        // Set up the gameStateManager
        gameStateManager = GameStateManager.getInstance();

    }

    /**
     * Get the arena instance
     */
    public static Arena getInstance() {
        if (instance == null) {
            instance = new Arena();
        }

        return instance;
    }

    @Override
    public void run() {

        // Init the field
        Logger.log("Arena", "Doing full field init");
        init();

        // Update components
        Logger.log("Arena", "Starting field loop");
        while (true) {
            update();
        }

    }

    /**
     * Fully init the field from scratch
     */
    private void init() {

    }

    /**
     * Set up everything for a new match
     */
    private void initMatch() {

    }

    /**
     * Update all field components
     */
    private void update() {

        // Update the gameStateManager
        gameStateManager.update();

        // Check if a packet should be pushed to driverstations
        if (gameStateManager.shouldPushDSPacket()) {

        }

    }

    /**
     * Push a packet to all connected driverstations.
     * 
     * I don't think this matters, but technically, the red alliance will always
     * have a very slight advantage.
     */
    private void pushDSPacket(ControlPacket packet) {

        // Red alliance
        for (AllianceStation station : redAlliance.getAllStations()) {
            // Ignore bypassed stations
            if (!station.bypassed) {
                station.driverstation.sendPacket(packet);
            }
        }

        // Blue alliance
        for (AllianceStation station : blueAlliance.getAllStations()) {
            // Ignore bypassed stations
            if (!station.bypassed) {
                station.driverstation.sendPacket(packet);
            }
        }

    }

}