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
        # this will be filled in correctly later
        self.vehicle = "🤡"
        self.visualizer = Visualizer(utils.getBuoysAbs(self.task))
        self.initRunMethod()

    def run(self):
        while True:
            velocity = self.runMethod()
            self.visualizer.animate(velocity)
            time.sleep(FC.Refresh_Sec)
    
    def initRunMethod(self):
        if self.task == 'NavChannelDemo':
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        closestBuoys = utils.findClosestBuoys(utils.getBuoysAbs('NavChannelDemo'))
        avgX = (closestBuoys['Red'].center[0] + closestBuoys['Green'].center[0]) / 2
        # https://dronekit-python.readthedocs.io/en/latest/automodule.html#dronekit.Vehicle.commands
        # TODO: this velocity needs to be normalized, otherwise speeds will be too high
        # utils.send_ned_velocity(self.vehicle, [(avgX - Constants.FRAME_WIDTH / 2) * Constants.VELOCITY_SCALE, 10, 0], 0)
        return [(avgX - Constants.FRAME_WIDTH / 2) * Constants.VELOCITY_SCALE, 10]