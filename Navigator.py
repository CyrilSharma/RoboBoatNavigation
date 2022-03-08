import utils
from Boat import Boat
from Visualize import Visualizer
import time
import Constants
import FrameConstants as FC

class SimulatedNavigator():
    def __init__(self, task, **kwargs):
        self.task = task
        self.initialize(kwargs)

    def initialize(self, kwargs):
        self.boat = Boat(kwargs.get('boatInit', [0, 0]))
        self.visualizer = Visualizer(self.boat, utils.getBuoysAbs(self.task))
        self.buoys = utils.getBuoysAbs(self.task)
        self.initRunMethod()

    def run(self):
        while True:
            velocity = self.runMethod()
            update = self.boat.update(velocity, FC.Refresh_Sec)
            self.visualizer.animate(update)
            time.sleep(FC.Refresh_Sec)
    
    def initRunMethod(self):
        if self.task == 'NavChannelDemo':
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        closestBuoys = utils.findClosestBuoys(utils.absPosToFrame(self.buoys, self.boat))
        if closestBuoys is None:
            return [0, 0]
        avgX = (closestBuoys['Red'].x + closestBuoys['Green'].x) / 2
        return [(avgX - Constants.FRAME_WIDTH / 2) * Constants.VELOCITY_SCALE, 10]