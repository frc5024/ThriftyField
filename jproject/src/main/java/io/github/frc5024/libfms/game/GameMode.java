package io.github.frc5024.libfms.game;

/**
 * Field game and setup modes
 */
public enum GameMode {
    PRE_MATCH, // Allowing robot connections, field being set up
    MATCH_START, // 3 second countdown
    AUTONOMOUS, // Autonomous period
    READY_PAUSE, // 1.5 second pause for drivers to pick up controllers
    TELEOP, // Teleop period
    ENDGAME, // 30 seconds from game end
    POST_MATCH; // Kick all robots off field, awaiting scores
}