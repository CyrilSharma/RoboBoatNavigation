import math

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
        if accl[0] == 0 and accl[1] == 0:
            return [0, 0]
        self.theta += accl[1] * dt
        self.vx += accl[0] * dt
        self.vy += accl[1] * dt
        dx = (self.vx * math.cos(self.theta) + self.vy * math.sin(self.theta)) * dt
        dy = (self.vx * math.sin(self.theta) + self.vy * math.cos(self.theta)) * dt
        self.x += dx
        self.y += dy
        return [dx, dy]