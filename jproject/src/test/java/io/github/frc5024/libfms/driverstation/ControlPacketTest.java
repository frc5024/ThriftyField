package io.github.frc5024.libfms.driverstation;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

import io.github.frc5024.libfms.driverstation.ControlPacket.RobotState;

public class ControlPacketTest {

    @Test
    public void testRobotStateFlagBuilding() {
        assertTrue("Default flag is 0x00", RobotState.buildFlag() == 0x00);
        assertTrue("DISABLED flag is 0x00", RobotState.buildFlag(RobotState.DISABLED) == 0x00);
        assertTrue("Autonomous mode flag is 0x06",
                RobotState.buildFlag(RobotState.AUTONOMOUS, RobotState.ENABLED) == 0x06);
        assertTrue("Estopped flag is 0x80", RobotState.buildFlag(RobotState.DISABLED, RobotState.ESTOPPED) == 0x80);
    }
}