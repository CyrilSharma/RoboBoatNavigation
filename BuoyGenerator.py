import random
import FrameConstants as FC
import Constants as C

def generateBuoys(mission: str):
    buoys = {}
    if mission.lower() == 'navchanneldemo':
        horizontal_space = random.randint(10, 16)
        vertical_space = random.randint(25, 100)
