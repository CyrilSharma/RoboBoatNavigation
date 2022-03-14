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

def isCloseEnough(pair1, pair2):
    if pair1 is None or pair2 is None:
        return False
    if None in pair1 or None in pair2:
        return False
    dist1 = math.sqrt((pair1['Red'].x - pair2['Red'].x)**2 + (pair1['Red'].y - pair2['Red'].y)**2)
    dist2 = math.sqrt((pair1['Green'].x - pair2['Green'].x)**2 + (pair1['Green'].y - pair2['Green'].y)**2)
     #.x - pair2.x)**2 + (pair1.y - pair2.y)**2)
    return (dist1 + dist2 < 100)

# find closest buoy with specific color
def findClosestBuoyPair(buoyList, pastBuoys, override=False):
    # buoys that appear the largest, are the closest
    if len(buoyList) < 1:
        return None

    # sort buoys by area
    redBuoyList = [buoy for buoy in buoyList if buoy.color == 'Red']
    greenBuoyList = [buoy for buoy in buoyList if buoy.color == 'Green']
    sortedRedBuoys = sorted(redBuoyList, key=lambda buoy: buoy.pixelData.width * buoy.pixelData.height, reverse=True)
    sortedGreenBuoys = sorted(greenBuoyList, key=lambda buoy: buoy.pixelData.width * buoy.pixelData.height, reverse=True)
    
    if len(sortedRedBuoys) < 1 or len(sortedGreenBuoys) < 1:
        return {"Red": None, "Green": None}

    redBuoy = None
    greenBuoy = None
    if len(sortedRedBuoys) > 0:
        redBuoy = sortedRedBuoys[0].pixelData
    if len(sortedGreenBuoys) > 0:
        greenBuoy = sortedGreenBuoys[0].pixelData
    buoys = {"Red": redBuoy, "Green": greenBuoy}

    """ if not isCloseEnough(pastBuoys, buoys) and not override:
        redBuoy = None
        greenBuoy = None
        if len(sortedRedBuoys) >= 2:
            redBuoy = sortedRedBuoys[1]
        if len(sortedGreenBuoys) >= 2:
            greenBuoy = sortedGreenBuoys[1]
        buoys = {"Red": redBuoy, "Green": greenBuoy} """

    return buoys

def updateFrame(buoyList, boat):
    updatedList = []
    for buoy in buoyList:
        dx = buoy.x - boat.x
        dy = buoy.y - boat.y
        buoyTheta = math.atan2(dy, dx)
        dTheta = buoyTheta - boat.theta
        dTheta = (dTheta + math.pi) % (2 * math.pi) - math.pi
        cutoffAngle = math.pi / 2.5
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