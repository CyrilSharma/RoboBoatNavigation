import math
import json
import Constants
import Buoy

def getBuoys(task: str, pos: list):
    buoys = getBuoysAbs(task)
    return absPosToFrame(buoys, pos)

def getBuoysAbs(task: str):
    with open('BuoyPositions.json') as f:
        buoys = json.load(f)
    
    rects = []
    for color in buoys[task]:
        for buoy in buoys[task][color]:
            rects.append(Buoy(calculateCorners(buoy['center'], buoy['height'], buoy['width']), color))

    return rects

def absPosToFrame(buoys: Buoy, pos: list):
    rects = []
    for buoy in buoys:
        frame_corners = []
        for corner in buoy.corners:
            pixel_pos = [Constants.CAMERA_RATIO * (corner[0] - pos[0]), Constants.CAMERA_RATIO * (corner[2] - pos[2])]
            frame_corners.append(pixel_pos)
        rects.append(Buoy(frame_corners, buoy.color))
    return rects

def calculateCorners(center, height, width):
    # Y is constant from view.
    corners = []
    corners[0] = [center[0] + width/2 + height/2, center[1], center[2] + width/2 - height/2]
    corners[1] = [center[0] + width/2 - height/2, center[1], center[2] - width/2 - height/2]
    corners[2] = [center[0] - width/2 + height/2, center[1], center[2] - width/2 - height/2]
    corners[3] = [center[0] - width/2 - height/2, center[1], center[2] + width/2 - height/2]
    return corners