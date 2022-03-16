import time
import math
import Constants  # import constants
import FrameConstants as FC  # constants about video frame


# define a navigator class that contains methods for tasks
# navigate_channel returns acceleration vector to keep boat between buoys
class Navigator():
    # set the run method according to the task configuration passed in
    def __init__(self, config):
        self.init_run_method(config.task)
    
    # to be implemented by subclasses
    def run(self):
        pass

    # set method to turn according to task
    # defaults currently to navigate_channel
    def init_run_method(self, task):
        if task.lower() == 'navchanneldemo':
            self.run_method = self.navigate_channel
        elif task.lower() == 'avoidcrowds':
            self.run_method = self.navigate_channel
        elif 'test' in task.lower() or 'straight' in task.lower():
            self.run_method = self.navigate_channel
        else:
            raise Exception("Invalid task")

    # returns acceleration vector 
    # accesses closest buoys attribute of navigator (set by Boat)
    def navigate_channel(self):
        # get the closest buoys, set by Boat
        closestBuoys = self.closestbuoys
        
        # physics blackbox
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
            aDelta = [attraction, 1]
            rDelta = [repulsion, 0]
            return normalize(add_vectors(aDelta, rDelta), Constants.MAX_ACCELERATION)
        elif None is closestBuoys['Red'] and None is closestBuoys['Green']:
            return [0,0]

        # (repulsive_force(-(redx - centerx)) + repulsive_force(-(greenx - centerx)))
        aDelta = [attraction, 1]
        rDelta = [repulsion, 0]

        # return acceleration 
        return normalize(add_vectors(aDelta, rDelta), Constants.MAX_ACCELERATION)

    # implemented by subclass
    def set_closest_buoys():
        pass
 
# Pixhawk navigator defines a subclass of navigator
# implements set_closest_buoys() and run()
class PixhawkNavigator(Navigator):
    
    def __init__(self, config):
        self.initRunMethod(config.task)

    # this can be made part of boat class
    def run(self):
        return self.runMethod()
            
    # generic setter method to set buoys
    # buoys is a dictionary of Buoy objects {'red': Buoy, 'green': Buoy}
    def set_closest_buoys(buoys):
        self.closestbuoys = buoys
  
# utility methods

def add_vectors(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]   

def normalize(vec, scale):
    mag = math.sqrt(vec[0]**2 + vec[1]**2)
    return [vec[0] * scale / mag, vec[1] * scale / mag]

def repulsive_force(diff):
    if abs(diff) < 200:
        return 1 * math.copysign(1, diff)
    return 0
