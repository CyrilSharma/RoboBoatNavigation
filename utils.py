import math
import json
from SimConfig import Config
import Constants
import FrameConstants as FC
from Buoy import Buoy
from pymavlink import mavutil
import time

def loadConfig(task: str):
    with open('BuoyPositions.json') as f:
        data = json.load(f)
        task = task.lower()
        boatPos = data[task]['Boat']['Position']
        boatTheta = data[task]['Boat']['Theta']
        buoys = []
        for color in data[task.lower()]:
            if (color == 'Boat'):
                continue
            for pos in data[task][color]:
                buoys.append(Buoy(pos, color))
    return Config(task, boatPos, boatTheta, buoys)

# find closest buoy with specific color
def findClosestBuoys(buoyList):
    # buoys that appear the largest, are the closest
    if len(buoyList) < 1:
        return None

    closestBuoys = []
    maxAreas = [-1,-1]
    for buoy in buoyList:
        area = buoy.pixelData.width * buoy.pixelData.height
        if buoy.color == 'Red':
            if area > maxAreas[0]:
                maxAreas[0] = area
                closestBuoys.append(buoy)
        elif buoy.color == 'Green':
            if area > maxAreas[1]:
                maxAreas[1] = area
                closestBuoys.append(buoy)
        
    buoys = {}
    for buoy in closestBuoys:
        if buoy.color not in closestBuoys:
            buoys[buoy.color] = buoy
    return buoys

def absPosToFrame(buoyList, boat):
    updatedList = []
    for buoy in buoyList:
        dx = buoy.x - boat.x
        dy = buoy.y - boat.y
        buoyTheta = math.atan2(dy, dx)
        dTheta = buoyTheta - boat.theta
        dTheta = (dTheta + math.pi) % (2 * math.pi) - math.pi
        cutoffAngle = math.pi / 3
        if (dTheta < -cutoffAngle or dTheta > cutoffAngle):
            continue
        dist = math.sqrt(dx**2 + dy**2)
        dx2 = dist * math.sin(dTheta)
        dy2 = dist * math.cos(dTheta)
        frameWidth = FC.Window_Width
        frameOffset = frameWidth*0.5 / math.tan(cutoffAngle)
        scale = frameOffset / dy2
        center = [frameWidth / 2 + dx2 * scale, buoy.height*scale/2]
        buoy.updatePixelData(center, buoy.width*scale, buoy.height*scale)
        updatedList.append(buoy)
    return updatedList

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