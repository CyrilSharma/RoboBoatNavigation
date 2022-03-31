# author Pearson Frank
# adapted from code by Cyril Sharma

import time
import math
import constants  # import constants


# buoy is a tuple (area, x, y)


# define a navigator class that contains methods for tasks
# navigate_channel returns acceleration vector to keep boat between buoys
class Navigator():
    # set the run method according to the task configuration passed in
    def __init__(self, config):
        self.closest_buoys = None
        self.window_width, self.window_height = config.frame_width, config.frame_height
        self.init_run_method(config.task)

    # to be implemented by subclasses
    def run(self):
        self.run_method()

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
        closest_buoys = self.closest_buoys

        # physics blackbox
        if closest_buoys is None:
            return [0, 0]
        elif closest_buoys['Red'] is not None and closest_buoys['Green'] is not None:
            centerx = self.window_width * 0.5
            redx = closest_buoys['Red'][1]
            red_area = closest_buoys['Red'][0]
            greenx = closest_buoys['Green'][1]
            green_area = closest_buoys['Green'][0]

            weight_degree = 0.9
            weight = (weight_degree * green_area + (1 - weight_degree) * red_area) / (red_area + green_area)
            weighted_x = (weight * redx + (1 - weight) * greenx)
            attraction = (weighted_x - centerx) * 0.1
            repulsion = 0
        elif None is not closest_buoys['Red'] or None is not closest_buoys['Green']:
            attraction = 0
            repulsion = 0
            for color in closest_buoys:
                buoy = closest_buoys[color]
            a_delta = [attraction, 1]
            r_delta = [repulsion, 0]
            return normalize(add_vectors(a_delta, r_delta), constants.MAX_ACCELERATION)
        elif None is closest_buoys['Red'] and None is closest_buoys['Green']:
            return [0, 0]

        # (repulsive_force(-(redx - centerx)) + repulsive_force(-(greenx - centerx)))
        a_delta = [attraction, 1]
        r_delta = [repulsion, 0]

        # return acceleration
        return normalize(add_vectors(a_delta, r_delta), constants.MAX_ACCELERATION)

    # implemented by subclass
    def set_closest_buoys(self, buoys):
        self.closest_buoys = buoys


# utility methods

def add_vectors(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]


def normalize(vec, scale):
    mag = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    return [vec[0] * scale / mag, vec[1] * scale / mag]


def repulsive_force(diff):
    if abs(diff) < 200:
        return 1 * math.copysign(1, diff)
    return 0
