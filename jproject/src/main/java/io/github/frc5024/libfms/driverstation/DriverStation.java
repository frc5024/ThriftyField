package io.github.frc5024.libfms.driverstation;

import io.github.frc5024.libfms.interfaces.Estoppable;
import io.github.frc5024.libfms.model.Team;

public class DriverStation implements Estoppable {

    public DriverStation(Team team, String hostAddress) {

    }

    @Override
    public void estop() {
        // TODO Auto-generated method stub

    }

    @Override
    public boolean isEstopped() {
        // TODO Auto-generated method stub
        return false;
    }

}