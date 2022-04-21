import tkinter
import utils
from SimulatedBoat import SimulatedBoat
from Boat import Boat
from Visualize import TopDownVisualizer, CameraVisualizer, WindowException
import time
import math
import Constants
import FrameConstants as FC
import cv2
from pynput import keyboard
from cvBuoyFinder import findBuoys
from dronekit import connect

class Navigator():
    def __init__(self, config):
        self.cam = cv2.VideoCapture(0)
        self.vehicle = connect("/dev/serial0", wait_ready=True, baud=960000)
        self.initRunMethod(config.task)
    
    def run(self):
        while True:
            accl = self.runMethod()
            print(accl)
            velocity = self.vehicle.velocity
            print(velocity)
            newVel = [velocity[0] + accl[0] * Constants.UPDATE_FREQ, velocity[1] + accl[1] * Constants.UPDATE_FREQ]
            print(newVel)
            # send new Velocity
            time.sleep(Constants.UPDATE_FREQ)

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
        closestBuoys = self.getClosestBuoys()
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

        return normalize(addVectors(aDelta, rDelta), Constants.MAX_ACCELERATION)

    def getClosestBuoys(self):
        return utils.findClosestRealBuoyPair(findBuoys(self.cam))

class SimulatedNavigator(Navigator):
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
    
    def getClosestBuoys(self):
        return utils.findClosestBuoyPair(utils.updateFrame(self.buoys, self.boat))

class PixhawkNavigator():
    def __init__(self, config):
        self.boat = Boat(None)
        self.initRunMethod(config.task)

    def run(self):
        while True:
            accl = self.runMethod()
            cur_vel = self.boat.velocity
            new_vel = [cur_vel[0] + accl[0] * Constants.UPDATE_FREQ, cur_vel[1] + accl[1] * Constants.UPDATE_FREQ]
            self.boat.send_velocity(new_vel)
            time.sleep(Constants.UPDATE_FREQ)
    
    def getClosestBuoys():
        # CV component goes here
        pass

def addVectors(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]   

def normalize(vec, scale):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    return [vec[0] * scale / mag, vec[1] * scale / mag]

def repulsiveForce(diff):
    if abs(diff) < 200:
        return 1 * math.copysign(1, diff)
    return 0
