import math
import json
import Constants
import Buoy

def getBuoys(task: str):
    buoys = getBuoysAbs(task)
    return absPosToFrame(buoys, Constants.CAMERA_POS)

def getBuoysAbs(task: str):
    with open('BuoyPositions.json') as f:
        buoys = json.load(f)
    rects = [calculateCorners(buoy, Constants.BUOY_HEIGHT, Constants.BUOY_WIDTH) for buoy in buoys[task]]
    return rects

def absPosToFrame(buoys: list, pos: list):
    rectangles = []
    for buoy in buoys:
        frame_corners = []
        for corner in buoy.corners:
            pixel_pos = [Constants.CAMERA_RATIO * (corner[0] - pos[0]), Constants.CAMERA_RATIO * (corner[2] - pos[2])]
            frame_corners.append(pixel_pos)
        rectangles.append(Buoy(frame_corners))
    return rectangles

def calculateCorners(center, height, width):
    # Y is constant from view.
    corners = []
    corners[0] = [center[0] + width/2 + height/2, center[1], center[2] + width/2 - height/2]
    corners[1] = [center[0] + width/2 - height/2, center[1], center[2] - width/2 - height/2]
    corners[2] = [center[0] - width/2 + height/2, center[1], center[2] - width/2 - height/2]
    corners[3] = [center[0] - width/2 - height/2, center[1], center[2] + width/2 - height/2]
    return corners