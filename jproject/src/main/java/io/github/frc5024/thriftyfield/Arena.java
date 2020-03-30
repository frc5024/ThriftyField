package io.github.frc5024.thriftyfield;

/**
 * The arena contains everything on the field
 */
public class Arena implements Runnable {
    private static Arena instance;

    

    private Arena() {

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