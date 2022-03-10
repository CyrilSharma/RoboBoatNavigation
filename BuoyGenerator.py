import random
from Buoy import Buoy
from SimConfig import Config
import FrameConstants as FC
import Constants as C
import math

def generateBuoys(task: str, seed: int = None):
    if task.lower() == 'navchanneldemo':
        config = generateNavDemo(task, seed)
    elif task.lower() == 'avoidcrowds':
        config = generateAvoidCrowds(task, seed)
    else:
        raise Exception("Invalid task")
    return config

def generateNavDemo(task, seed: int = None):
    if seed is not None:
        random.seed(seed)

    centerX = FC.Window_Width/2
    horizontal_offset = random.randint(5, 15)
    vertical_offset = random.randint(20, 50)
    min_y = 50

    buoys = []

    greenBuoys = [[centerX - horizontal_offset - C.BUOY_WIDTH, min_y], [centerX - horizontal_offset - C.BUOY_WIDTH, min_y + vertical_offset]]
    for i in greenBuoys:
        buoys.append(Buoy(i, 'Green'))
    
    redBuoys = [[centerX + horizontal_offset, min_y], [centerX + horizontal_offset, min_y + vertical_offset]]
    for i in redBuoys:
        buoys.append(Buoy(i, 'Red'))

    boatPosition = [centerX - C.BOAT_SIZE[0]/2, 20]
    boatTheta = math.pi / 2

    return Config(task, boatPosition, boatTheta, buoys)

def generateAvoidCrowds(task, seed: int = None):
    if seed is not None:
        random.seed(seed)

    centerX = FC.Window_Width / 2
    offset = 10
    fluctuationSize = 10
    numBuoys = 25
    xpositions = []
    integral = 0

    for i in range(numBuoys):
        integral += random.randint(-1, 1) * fluctuationSize
        xpositions.append(int(centerX - offset + integral))

    buoys = []
    y = 50
    for i in range(numBuoys):
        x = xpositions[i]
        buoys.append(Buoy([x, y + random.randint(-1, 1)], 'Green'))
        buoys.append(Buoy([x + 2 * offset, y + random.randint(-1, 1)], 'Red'))
        y += 20

    boatPosition = [FC.Window_Width / 2, 20]
    boatTheta = math.pi / 2
    return Config(task, boatPosition, boatTheta, buoys)
