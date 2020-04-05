package io.github.frc5024.thriftyfield.gameplay;

import io.github.frc5024.libfms.game.GameMode;

public class GameStateManager {

    private static GameStateManager instance;

    private GameStateManager() {

    }

    public static GameStateManager getInstance() {
        if (instance == null) {
            instance = new GameStateManager();
        }

        return instance;
    }

    public void startGame() {
        startGame(GameMode.AUTONOMOUS);
    }

    public void startGame(GameMode mode) {

    }
    
    public void abortGame() {
        
    }

    public void update() {

    }
    
    public boolean isMatchPlaying() {
        return false;
    }

    public boolean shouldPushDSPacket(){
        return false;
    }
}