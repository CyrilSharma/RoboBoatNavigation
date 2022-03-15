import math

class Config():
    def __init__(self, task=None, pixhawk=False, boatPos=[0, 0], boatTheta=math.pi/2, buoys=None):
        self.task = task
        self.pixhawk = pixhawk
        self.boatPos = boatPos
        self.boatTheta = boatTheta
        self.buoys = buoys