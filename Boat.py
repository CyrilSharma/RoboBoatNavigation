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
    
    def update(self, velocity, dt):
        if velocity[0] == 0 and velocity[1] == 0:
            return [0, 0]
        self.theta = math.atan2(velocity[1], velocity[0])
        self.x += velocity[0] * dt
        self.y += velocity[1] * dt
        self.vx = velocity[0]
        self.vy = velocity[1]
        return [velocity[0] * dt, velocity[1] * dt]