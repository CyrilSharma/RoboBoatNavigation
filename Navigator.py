import utils
from Visualize import Visualizer
import time
import Constants
import FrameConstants as FC

class SimulatedNavigator():
    def __init__(self, task):
        self.task = task
        self.initialize()
    
    def initialize(self):
        self.visualizer = Visualizer(utils.getBuoysAbs(self.task))
        self.boatPos = [0,0,Constants.BUOY_HEIGHT / 2]
        self.buoys = utils.getBuoysAbs(self.task)
        self.initRunMethod()

    def run(self):
        while True:
            velocity = self.runMethod()
            self.boatPos = [self.boatPos[0] + velocity[0] * FC.Refresh_Sec, self.boatPos[1] + velocity[1] * FC.Refresh_Sec, Constants.BUOY_HEIGHT / 2]
            print(velocity)
            self.visualizer.animate(velocity)
            time.sleep(FC.Refresh_Sec)
    
    def initRunMethod(self):
        if self.task == 'NavChannelDemo':
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        closestBuoys = utils.absPosToFrame(self.buoys, self.boatPos)
        avgX = (closestBuoys['Red'].center[0] + closestBuoys['Green'].center[0]) / 2
        return [(avgX - Constants.FRAME_WIDTH / 2) * Constants.VELOCITY_SCALE, 10]