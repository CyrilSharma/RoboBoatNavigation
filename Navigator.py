import utils
from Boat import Boat
import time
import math
import Constants
import FrameConstants as FC
from pynput import keyboard

class Navigator():
    def __init__(self, config):
        self.initRunMethod(config.task)
    
    def run(self):
        pass

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

    def getClosestBuoys():
        pass

class PixhawkNavigator(Navigator):
    # entry point
    
    def __init__(self, config):
        self.initRunMethod(config.task)

    # this can be made part of boat class
    def run(self):
        while True:
            accl = self.runMethod()
            cur_vel = self.boat.velocity
            new_vel = [cur_vel[0] + accl[0] * Constants.UPDATE_FREQ, cur_vel[1] + accl[1] * Constants.UPDATE_FREQ]
            # return a velocity
            self.boat.send_velocity(new_vel)
            time.sleep(Constants.UPDATE_FREQ)
    
    def getVelocityUpdate():
        # return a velocity
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
