import math
import Constants
class Boat():
    def __init__(self, position=[0,0], theta=math.pi/2):
        self.x = position[0]
        self.y = position[1]
        self.theta = theta
        self.vx = 0
        self.vy = 0
        self.width = 10
        self.height = 10
        self.color = 'Red'
    
    # remake system so that it moves in direction of orientation
    def update(self, accl, dt):
        self.theta += accl[0] * dt
        self.vx += accl[0] * dt
        self.vy += accl[1] * dt
        if (abs(self.vx) > Constants.MAX_SPEED):
            self.vx = Constants.MAX_SPEED * math.copysign(1, self.vx)
        if (abs(self.vy) > Constants.MAX_SPEED):
            self.vy = Constants.MAX_SPEED * math.copysign(1, self.vy)

        dx = (self.vy * math.cos(self.theta) + self.vx * math.sin(self.theta)) * dt
        dy = (self.vy * math.sin(self.theta) + self.vx * math.cos(self.theta)) * dt
        self.x += dx
        self.y += dy
        return [dx, dy]