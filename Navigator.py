import utils
from Boat import Boat
from Visualize import TopDownVisualizer, CameraVisualizer, WindowException
import time
import math
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
        global playing
        playing = True

        def on_press(key):
            if key == keyboard.Key.space:
                global playing
                playing = not playing

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while True:
            if not playing:
                continue
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
        centerx = FC.Window_Width * 0.5
        redx = closestBuoys['Red'].pixelData.x
        greenx = closestBuoys['Green'].pixelData.x
        avgX = (redx + greenx) / 2
        attraction = (avgX - centerx) * 0.1
        repulsion =  (repulsiveForce(-(redx - centerx)) + repulsiveForce(-(greenx - centerx)))
        delta1 = [attraction, 1]
        delta2 = numToVec(repulsion,1)
        print(f"red: {repulsiveForce(-(redx - centerx))} | green: {repulsiveForce(-(greenx - centerx))} | {delta1} | {delta2}")

        return normalize(addVectors(delta1, delta2), Constants.MAX_ACCELERATION)  

def addVectors(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]   

def normalize(vec, scale):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    return [vec[0] * scale / mag, vec[1] * scale / mag]
    
def numToVec(delta, scale):
    # map number to [0, pi]
    theta = math.pi * sigmoid(delta)
    return [math.cos(theta) * scale, math.sin(theta) * scale]

def sigmoid(x):
    sig = 1 / (1 + math.exp(-x * 30))
    return sig

def repulsiveForce(diff):
    force = math.copysign(1, diff) / (((0.5*diff)**2) + 0.1)
    return force