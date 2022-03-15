import dronekit as dk
from dronekit import mavutil
import Constants
from Navigator import PixhawkNavigator
from Buoy import Buoy
# import cv


class Boat():
    # port name like /dev/ttyAMA0
    def __init__(self, port_name, name, baudrate):
        self.id = name
        self.vehicle = dk.connect(port_name=None, baud=baudrate, wait_ready=True)
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
        self.position = self.vehicle.location.local_frame  # NED (N=y, E=x)
        self.velocity = self.vehicle.velocity  # [vx, vy, vz]
        self.heading = self.vehicle.heading  # [0, 360] where 0 degrees North

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

    def run_navigator(config):
        # create navigator, pass config
        nav = PixhawkNavigator(config)
        while True:
            nav.setClosestBuoys(self.get_closes_buoys())
            accl = nav.runMethod()
            cur_vel = self.velocity
            new_vel = [cur_vel[0] + accl[0] * Constants.UPDATE_FREQ, cur_vel[1] + accl[1] * Constants.UPDATE_FREQ]
            self.send_velocity(new_vel)
            self.updateState()
            time.sleep(Constants.UPDATE_FREQ)
    
    # from cv get positions relative to frame
    def get_closest_buoys:
        # create buoy objects
        pass
    # def get velocities
