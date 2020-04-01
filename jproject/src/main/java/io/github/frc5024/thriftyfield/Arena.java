package io.github.frc5024.thriftyfield;

import java.io.IOException;

import io.github.frc5024.libfms.driverstation.ConnectionListener;
import io.github.frc5024.util.Logger;

/**
 * The arena contains everything on the field
 */
public class Arena implements Runnable {
    private static Arena instance;

    // Driverstation connection listener
    private ConnectionListener dsConnectionListener;

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

    }

}