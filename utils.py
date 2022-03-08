import math
import json
import Constants
from Buoy import Buoy
from pymavlink import mavutil
import time

def getBuoysAbs(task: str):
    buoys = []
    with open('BuoyPositions.json') as f:
        data = json.load(f)
        for color in data[task]:
            for pos in data[task][color]:
                buoys.append(Buoy(pos, color))
    return buoys

# find closest buoy with specific color
def findClosestBuoys(buoyList):
    # buoys that appear the largest, are the closest
    if len(buoyList) < 1:
        return None
        
    closestBuoys = []
    maxArea = buoyList[0].width * buoyList[0].height
    for buoy in buoyList:
        area = buoy.width * buoy.height
        if (area >= maxArea):
            maxArea = area
            closestBuoys.append(buoy)
        
    buoys = {}
    for buoy in closestBuoys:
        if buoy.color not in closestBuoys:
            buoys[buoy.color] = buoy
    return buoys

def absPosToFrame(buoyList, boat):
    buoys = []
    for buoy in buoyList:
        dx = buoy.x - boat.x
        dy = buoy.y - boat.y
        buoyTheta = math.atan2(dy, dx)
        dTheta = buoyTheta - boat.theta
        dTheta = (dTheta + math.pi) % (2 * math.pi) - math.pi
        if (dTheta < -math.pi / 3 or dTheta > math.pi / 3):
            continue
        dist = math.sqrt(dx**2 + dy**2)
        dx2 = dist * math.sin(dTheta)
        dy2 = dist * math.cos(dTheta)
        scale = 10 / dy2
        center = [dx2 * scale, scale * buoy.height / 2]
        buoys.append(Buoy(center, buoy.color, width=buoy.width*scale, height=buoy.height*scale, corners=calculateCorners(center, buoy.height * scale, buoy.width * scale)))
    return buoys

def calculateCorners(center, height, width):
    # [X, Y, Z]
    # Y is constant from view.
    corners = []
    corners.append([center[0] + width/2, center[1] + height/2])
    corners.append([center[0] - width/2, center[1] + height/2])
    corners.append([center[0] + width/2, center[1] - height/2])
    corners.append([center[0] - width/2, center[1] - height/2])
    return corners

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