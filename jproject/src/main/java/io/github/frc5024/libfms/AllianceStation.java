package io.github.frc5024.libfms;

import io.github.frc5024.libfms.driverstation.DriverStation;
import io.github.frc5024.libfms.driverstation.ControlPacket.AllianceStationID;
import io.github.frc5024.libfms.interfaces.Estoppable;
import io.github.frc5024.libfms.model.Team;

public class AllianceStation implements Estoppable {

    public boolean estopped;
    public boolean bypassed;
    public Team team;
    public DriverStation driverstation;
    private AllianceStationID id;

    public AllianceStation(AllianceStationID id) {
        this.id = id;
    }

    /**
     * Set a new team for this station. Will clear existing driverstation
     * 
     * @param team Team to set
     */
    public void setTeam(Team team) {
        this.team = team;
        bypassed = false;
        estopped = false;
        driverstation = null;
    }

    public void connectDriverStation(String hostAddress) {
        driverstation = new DriverStation(team, id, hostAddress);
    }

    public void estop() {
        estopped = true;

        if (driverstation != null) {
            driverstation.estop();
        }
    }

    @Override
    public boolean isEstopped() {
        return estopped || (driverstation != null) ? driverstation.isEstopped() : false;
    }

    /**
     * Is this alliance station waiting for a team to connect?
     * 
     * @return Waiting for connection?
     */
    public boolean isWaitingForConnection() {
        return !bypassed && !isEstopped() && driverstation == null;
    }

}