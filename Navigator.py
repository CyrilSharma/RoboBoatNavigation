import utils
from Boat import Boat
from Visualize import TopDownVisualizer, CameraVisualizer
import time
import Constants
import FrameConstants as FC
from pynput import keyboard

class SimulatedNavigator():
    def __init__(self, task, **kwargs):
        self.task = task
        self.initialize(kwargs)

    def initialize(self, kwargs):
        self.boat = Boat(kwargs.get('boatInit', [0, 0]))
        self.visualizer = TopDownVisualizer(self.boat, utils.getBuoysAbs(self.task))
        self.cvisualizer = CameraVisualizer(utils.absPosToFrame(utils.getBuoysAbs(self.task), self.boat))
        self.buoys = utils.getBuoysAbs(self.task)
        self.initRunMethod()

    def run(self):
        block = False
        global playing
        playing = True

        def on_press(key):
            if key == keyboard.Key.space:
                global playing
                playing = not playing
                block = False

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while True:
            '''if keyboard.is_pressed(' '):
                if block == False:
                    playing = not playing
                    block = True
            else:
                block = False'''
            if playing:
                accl = self.runMethod()
                update = self.boat.update(accl, FC.Refresh_Sec)
                self.visualizer.animate(update)
                self.cvisualizer.update(utils.absPosToFrame(self.buoys, self.boat))
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
        elif 'Red' not in closestBuoys or 'Green' not in closestBuoys:
            return [0, 0]
        avgX = (closestBuoys['Red'].x + closestBuoys['Green'].x) / 2
        return [1,(avgX - FC.Window_Width / 2) * Constants.VELOCITY_SCALE]