import math

class Config():
    def __init__(self, task='NavChannelDemo', boatPos=[0, 0], boatTheta=math.pi/2, randomBuoys=False, seed=None):
        self.task = task
        self.boatPos = boatPos
        self.boatTheta = boatTheta
        self.randomBuoys = randomBuoys
        self.seed = seed