import math
import json
import Constants
from Buoy import Buoy
from pymavlink import mavutil
import time

# https://dronekit-python.readthedocs.io/en/latest/guide/copter/guided_mode.html
def send_ned_velocity(vehicle, velocity, duration):
    pass
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity[0], velocity[1], velocity[2], # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    # send command to vehicle on 1 Hz cycle
    for _ in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def getBuoysAbs(task: str):
    with open('BuoyPositions.json') as f:
        buoys = json.load(f)
    
    rects = {}
    for color in buoys[task]:
        rects[color] = []
        for buoy in buoys[task][color]:
            rects[color].append(Buoy(calculateCorners(buoy, Constants.BUOY_HEIGHT, Constants.BUOY_WIDTH), buoy, color))
    return rects

# find closest buoy with specific color
def findClosestBuoys(buoyList):
    closestBuoys = {}
    for color in buoyList:
        minDist = buoyList[color][0].center[1]
        for buoy in buoyList[color]:
            if (buoy.center[1] <= minDist):
                minDist = buoy.center[1]
                closestBuoys[color] = buoy
    return closestBuoys

def getBuoys(task: str, pos):
    buoys = getBuoysAbs(task)
    return absPosToFrame(buoys, pos)

# TODO: this doesn't do the projection quite right...
def absPosToFrame(buoys, pos):
    rects = {}
    for color in buoys:
        for buoy in buoys[color]:
            frame_corners = []
            for corner in buoy.corners:
                pixel_pos = [Constants.FRAME_OFFSET * (corner[0] - pos[0]), Constants.FRAME_OFFSET * (corner[2] - pos[2])]
                frame_corners.append(pixel_pos)
            rects[color] = Buoy(frame_corners, buoy.center, color)
    return rects

def calculateCorners(center, height, width):
    # [X, Y, Z]
    # Y is constant from view.
    corners = []
    corners.append([center[0] + width/2 + height/2, center[1], 0 + width/2 - height/2])
    corners.append([center[0] + width/2 - height/2, center[1], 0 - width/2 - height/2])
    corners.append([center[0] - width/2 + height/2, center[1], 0 - width/2 - height/2])
    corners.append([center[0] - width/2 - height/2, center[1], 0 + width/2 - height/2])
    return corners