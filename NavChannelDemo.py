import utils
from dronekit import Command
from pymavlink import mavutil
import Constants

def navigateChannel(vehicle):
    closestBuoys = findClosestBuoys(utils.getBuoysAbs('NavChannelDemo'))
    avgX = (closestBuoys['red'].position[0] + closestBuoys['green'].position[0]) / 2
    # https://dronekit-python.readthedocs.io/en/latest/automodule.html#dronekit.Vehicle.commands
    # TODO: this velocity needs to be normalized, otherwise speeds will be too high
    utils.send_ned_velocity(vehicle, [(avgX - Constants.FRAME_WIDTH / 2) * Constants.VELOCITY_SCALE, 10, 0], 0)

# find closest buoy with specific color
def findClosestBuoys(buoyList):
    closestBuoys = {}
    for color in buoyList:
        minDist = 0
        for buoy in buoyList[color]:
            if (buoy.center[2] < minDist):
                minDist = buoy.center[2]
                closestBuoys[color] = buoy
    return closestBuoys