import random
import FrameConstants as FC
import Constants as C

def generateBuoys(task: str, seed: int = None):
    if task.lower() == 'navchanneldemo':
        buoys = generateNavigationBuoys(seed)
    else:
        raise Exception("Invalid task")
    return buoys

def generateNavigationBuoys(seed: int = None):
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
        xpositions.append(centerX - offset + integral)

    for i in range(numBuoys):
        buoys = {}
        buoys['Red'] = []
        buoys['Green'] = []
        for x in xpositions:
            buoys['Red'].append(Buoy())
            buoys['Green'].append(Buoy())))
        centerX + xpositions[i]
        buoy['y'] = random.randint(0, FC.Window_Height)
        buoy['color'] = 'Red' if i % 2 == 0 else 'Green'
        buoy['id'] = i
        buoys[i] = buoy

    return buoys
