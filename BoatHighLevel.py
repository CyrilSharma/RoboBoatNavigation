import dronekit as dk
from dronekit import mavutil
# import navigation package
from Navigator import SimulatedNavigator, PixhawkNavigator
# import cv


class Boat():
    # port name like /dev/ttyAMA0
    def __init__(self, port_name, id):
        self.id = id
        self.vehicle = dk.connect(port_name=None, baud=57600, wait_ready=True)
        print('Successfully connected')
        self.check_in()
        self.updateState()
     
    def get_id(self):
        return self.id

    def check_in(self):
        print("Vehicle state:")
        print(f" GPS: {self.vehicle.gps_0}")
        print(f" Battery: {self.vehicle.battery}")
        print(f" Last Heartbeat: {self.vehicle.last_heartbeat}")
        print(f" System status: {self.vehicle.system_status.state}")
        print(f" Mode: {self.vehicle.mode.name}")
        print(f" Local location: {self.vehicle.location.local_frame}")
        print(f" Velocity: {self.vehicle.velocity}")
    
    def updateState(self):
        self.position = self.vehicle.location.local_frame
        self.velocity = self.vehicle.velocity
        self.heading = self.vehicle.heading

    # velocity as a list
    # local velocity
    def send_velocity(self, velocity):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,  # time_boot_ms (not used)
            0, 0,  # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111000111,  # type_mask (only speeds enabled)
            0, 0, 0,  # x, y, z positions (not used)
            velocity[0], velocity[1], velocity[2],  # x, y, z velocity in m/s
            0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        self.vehicle.send_mavlink(msg)

    # relative coordinates to beginning position in NED
    # North (x), East (y), Down (z) (not used)
    def get_position(self):
        return self.vehicle.location.local_frame
    
    # returns velocity as [vx, vy, vz] in m/s
    def get_velocity(self):
        return self.vehicle.velocity
    
    # returns current heading in degrees [0, 360] where 0 deg is N
    def get_heading(self):
        return self.vehicle.heading
    
    
    # def get_buoy_positions
    # from cv get positions relative to frame

    # def get velocities
