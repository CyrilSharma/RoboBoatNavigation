import utils
from Boat import Boat
from Visualize import TopDownVisualizer, CameraVisualizer
import time
import Constants
import FrameConstants as FC
from pynput import keyboard
class SimulatedNavigator():
    def __init__(self, config):
        self.boat = Boat(config.boatPos, config.boatTheta)
        self.buoys = utils.absPosToFrame(config.buoys, self.boat)
        self.visualizer = TopDownVisualizer(self.buoys, self.boat)
        self.cvisualizer = CameraVisualizer()
        self.initRunMethod(config.task)

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
            if playing:
                try: 
                    accl = self.runMethod()
                    update = self.boat.update(accl, FC.Refresh_Sec)
                    self.visualizer.animate(update)
                    self.cvisualizer.update(utils.absPosToFrame(self.buoys, self.boat), self.boat)
                    time.sleep(FC.Refresh_Sec)
                except Exception as e:
                    break
    
    def initRunMethod(self, task):
        if task.lower() == 'navchanneldemo':
            self.runMethod = self.navigateChannel
        elif task.lower() == 'avoidcrowds':
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        closestBuoys = utils.findClosestBuoys(utils.absPosToFrame(self.buoys, self.boat))
        if closestBuoys is None:
            return [0, 0]
        elif 'Red' not in closestBuoys or 'Green' not in closestBuoys:
            return [0, 0]
        avgX = (closestBuoys['Red'].pixelData.x + closestBuoys['Green'].pixelData.x) / 2
        return [1.5,(avgX - FC.Window_Width / 2) * Constants.VELOCITY_SCALE]