# Source code from Cyril Sharma
# adapted Pearson Frank
# defines a Boat class that connects to pixhawk, updates boat velocity using navigator, and integrates CV buoy detection

import dronekit as dk  # dronekit is the base API for connecting to pixhawk
from dronekit import mavutil  # mavutil manages mavlink connection to pixhawk
import Constants  # contains relevant information about buoys sizes and boat
from Navigator import PixhawkNavigator  # pixhawknavigator manages getting new velocity from buoys
from Buoy import Buoy  # buoy object has attributes for color and center x, y 
# import cv  # code written by Lexie Skeen and Sydney Belt for buoy detection


class Boat():
    # port name like /dev/ttyAMA0 for serial connection
    # name is an arbitrary ID for the Pixhawk
    def __init__(self, port_name, name, baudrate):
        self.id = name
        self.vehicle = dk.connect(port_name=None, baud=baudrate, wait_ready=True)  # creates a dronekit vehicle object associated with this boat object
        print('Successfully connected')
        self.original_pos = self.vehicle.location.global_frame  # store the starting global position (lat, long) just in case, since all other positions are relative
        self.check_in()  # print a few things about the boat
        self.update_state()  # set the state of the boat object 
     
    # return boat id
    def get_id(self):
        return self.id

    # print to terminal some boat.vehicle aspects
    def check_in(self):
        print("Vehicle state:")
        print(f" GPS: {self.vehicle.gps_0}")
        print(f" Battery: {self.vehicle.battery}")
        print(f" Last Heartbeat: {self.vehicle.last_heartbeat}")
        print(f" System status: {self.vehicle.system_status.state}")
        print(f" Mode: {self.vehicle.mode.name}")
        print(f" Local location: {self.vehicle.location.local_frame}")
        print(f" Velocity: {self.vehicle.velocity}")
    
    # set boat position, velocity, and heading to those of self.vehicle
    # makes it easier to call self.position instead of self.vehicle.location.local_frame etc
    # call every time velocity is updated
    def update_state(self):
        self.position = self.vehicle.location.local_frame  # NED (N=y, E=x)
        self.velocity = self.vehicle.velocity  # [vx, vy, vz]
        self.heading = self.vehicle.heading  # [0, 360] where 0 degrees North

    # velocity is a list [vx, vy]
    # vz automatically 0, the boat doesn't go up or down
    # uses dronekit message factory to create a mavlink message
    # see https://dronekit-python.readthedocs.io/en/latest/guide/copter/guided_mode.html "velocity control" for more
    def send_velocity(self, velocity):
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,  # time_boot_ms (not used)
            0, 0,  # target system, target component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111000111,  # type_mask (only speeds enabled)
            0, 0, 0,  # x, y, z positions (not used)
            velocity[0], velocity[1], 0,  # x, y, z velocity in m/s
            0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
        self.vehicle.send_mavlink(msg)  # send the message to the vehicle

    # method to be called once
    # pass in a config object, which contains infomration about the vehicle task
    # creates a navigator object and continuously updates velocity
    # --!-- might change to eliminate while True for other tasks --!--
    def run_navigator(config):
        nav = PixhawkNavigator(config)  # create navigator, pass config
        while True:  # do this forever
            nav.set_closest_buoys(self.get_closest_buoys())  # set the nav closest buoys to those found by CV (see get_closest_buoys)   
            self.update_state()  # get latest position information
            accl = nav.run_method()  # run main nav method to get the acceleration
            cur_vel = self.velocity  # current vehicle velocity
            new_vel = [cur_vel[0] + accl[0] * Constants.UPDATE_FREQ, cur_vel[1] + accl[1] * Constants.UPDATE_FREQ]  # update velocity proportional to how often we update
            self.send_velocity(new_vel)  # push the velocity to pixhawk
            time.sleep(Constants.UPDATE_FREQ)  # pause for a little bit
    
    # from cv get positions relative to frame
    # return a dictionary of Buoy objects {'red': Buoy, 'green': Buoy}
    def get_closest_buoys:
        # create buoy objects
        pass
