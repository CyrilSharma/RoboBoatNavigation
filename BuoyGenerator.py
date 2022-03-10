import random
from Config import Config
import FrameConstants as FC
import Constants as C
import math

def generateBuoys(task: str, seed: int = None):
    if task.lower() == 'navchanneldemo':
        config = generateNavDemo(seed)
    elif task.lower() == 'avoidcrowds':
        config = generateAvoidCrowds(seed)
    else:
        raise Exception("Invalid task")
    return config

def generateNavDemo(seed: int = None):
    if seed is not None:
        random.seed(seed)

    centerX = FC.Window_Width/2
    horizontal_offset = random.randint(5, 15)
    vertical_offset = random.randint(20, 50)
    min_y = 50

    buoys = {}
    buoys['Green'] = [[centerX - horizontal_offset - C.BUOY_WIDTH, min_y], [centerX - horizontal_offset - C.BUOY_WIDTH, min_y + vertical_offset]]
    buoys['Red'] = [[centerX - horizontal_offset, min_y], [centerX - horizontal_offset, min_y + vertical_offset]]

    boatPosition = [centerX - C.BOAT_SIZE[0]/2, 20]
    boatTheta = math.pi / 2
    return Config(boatPosition, boatTheta, buoys)

def generateAvoidCrowds(seed: int = None):
    if seed is not None:
        random.seed(seed)

    centerX = FC.Window_Width / 2
    offset = 10
    fluctuationSize = 10
    numBuoys = 25
    xpositions = []
    integral = 0

    for i in range(numBuoys):
        integral += random.randint(0, 1) * fluctuationSize
        xpositions.append(centerX - offset + integral // 1)

    for i in range(numBuoys):
        buoys = {}
        buoys['Red'] = []
        buoys['Green'] = []

        y = 50
        for x in xpositions:
            buoys['Red'].append([x, y + random.randint(-3, 3)])
            buoys['Green'].append([x + 2 * offset, y + random.randint(-3, 3)])
            y += 20
    
    boatPosition = [FC.Window_Width / 2, 20]
    boatTheta = math.pi / 2
    return Config(boatPosition, boatTheta, buoys)
