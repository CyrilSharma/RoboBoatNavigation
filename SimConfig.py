import math

class Config():
    def __init__(self, boatPos=[0, 0], boatTheta=math.pi/2, buoys=None):
        self.boatPos = boatPos
        self.boatTheta = boatTheta
        self.buoys = buoys