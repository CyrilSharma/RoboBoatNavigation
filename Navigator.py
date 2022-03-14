import tkinter
import utils
from SimulatedBoat import SimulatedBoat
from Visualize import TopDownVisualizer, CameraVisualizer, WindowException
import time
import math
import Constants
import FrameConstants as FC
from pynput import keyboard
class SimulatedNavigator():
    def __init__(self, config):
        self.boat = SimulatedBoat(config.boatPos, config.boatTheta)
        self.buoys = utils.updateFrame(config.buoys, self.boat)
        self.visualizer = TopDownVisualizer(self.buoys, self.boat)
        self.cvisualizer = CameraVisualizer()
        self.pastBuoys = None
        self.frameCount = 0
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
            try:
                if not playing:
                    continue
                accl = self.runMethod()
                update = self.boat.update(accl, FC.Refresh_Sec)
                self.visualizer.animate(update)
                self.cvisualizer.update(utils.updateFrame(self.buoys, self.boat), self.boat)
                time.sleep(FC.Refresh_Sec)
                self.frameCount += 1
            except tkinter.TclError:
                break

    
    def initRunMethod(self, task):
        if task.lower() == 'navchanneldemo':
            self.runMethod = self.navigateChannel
        elif task.lower() == 'avoidcrowds':
            self.runMethod = self.navigateChannel
        elif 'test' in task.lower() or 'straight' in task.lower():
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        closestBuoys = utils.findClosestBuoyPair(utils.updateFrame(self.buoys, self.boat), self.pastBuoys, self.frameCount==0)
        if closestBuoys is None:
            return [0, 0]
        elif closestBuoys['Red'] is not None and closestBuoys['Green'] is not None:
            centerx = FC.Window_Width * 0.5
            redx = closestBuoys['Red'].x 
            redArea = closestBuoys['Red'].width * closestBuoys['Red'].height
            greenx = closestBuoys['Green'].x
            greenArea = closestBuoys['Green'].width * closestBuoys['Green'].height

            weightDegree = 0.9
            weight = (weightDegree * greenArea + (1 - weightDegree) * redArea) / (redArea + greenArea)
            weightedX = (weight * redx + (1 - weight) * greenx)
            attraction = (weightedX - centerx) * 0.1
            repulsion = 0 
        elif None is not closestBuoys['Red'] or None is not closestBuoys['Green']:
            attraction = 0
            repulsion = 0
            for color in closestBuoys:
                buoy = closestBuoys[color]
                repulsion += repulsiveForce(-(buoy.x - centerx))
            aDelta = [attraction, 1]
            rDelta = [repulsion, 0]
            return normalize(addVectors(aDelta, rDelta), Constants.MAX_ACCELERATION)
        elif None is closestBuoys['Red'] and None is closestBuoys['Green']:
            return [0,0]

        # (repulsiveForce(-(redx - centerx)) + repulsiveForce(-(greenx - centerx)))
        aDelta = [attraction, 1]
        rDelta = [repulsion, 0]

        # save the buoy positions
        self.pastBuoys = closestBuoys

        return normalize(addVectors(aDelta, rDelta), Constants.MAX_ACCELERATION)

class PixhawkNavigator():
    def __init__(self, config):
        self.boat = SimulatedBoat(config.boatPos, config.boatTheta)
        self.frameCount = 0
        self.initRunMethod(config.task)

    def run(self):
        while True:
            accl = self.runMethod()
            time.sleep(FC.Refresh_Sec)

    
    def initRunMethod(self, task):
        if task.lower() == 'navchanneldemo':
            self.runMethod = self.navigateChannel
        elif task.lower() == 'avoidcrowds':
            self.runMethod = self.navigateChannel
        elif 'test' in task.lower() or 'straight' in task.lower():
            self.runMethod = self.navigateChannel
        else:
            raise Exception("Invalid task")

    def navigateChannel(self):
        # replace with CV component that fetches bounding boxes.
        closestBuoys = utils.findClosestBuoyPair(utils.updateFrame(self.buoys, self.boat), self.pastBuoys, self.frameCount==0)
        if closestBuoys is None:
            return [0, 0]
        elif None is closestBuoys['Red'] or None is closestBuoys['Green']:
            return [0, 0]

        centerx = FC.Window_Width * 0.5
        redx = closestBuoys['Red'].x 
        redArea = closestBuoys['Red'].width * closestBuoys['Red'].height
        greenx = closestBuoys['Green'].x
        greenArea = closestBuoys['Green'].width * closestBuoys['Green'].height
        weightDegree = 0.80
        weight = (weightDegree * greenArea + (1 - weightDegree) * redArea) / (redArea + greenArea)
        avgX = (weight * redx + (1 - weight) * greenx)
        attraction = (avgX - centerx) * 0.1

        repulsion = (repulsiveForce(-(redx - centerx)) + repulsiveForce(-(greenx - centerx)))
        delta1 = [attraction, 1]
        delta2 = [repulsion, 1]

        return normalize(addVectors(delta1, delta2), Constants.MAX_ACCELERATION)

def addVectors(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]   

def normalize(vec, scale):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    return [vec[0] * scale / mag, vec[1] * scale / mag]

def repulsiveForce(diff):
    if abs(diff) < 200:
        return 1 * math.copysign(1, diff)
    return 0
