import Constants
class Buoy():
    def __init__(self, center, color, width=None, height=None, corners=None):
        self.x = center[0]
        self.y = center[1]
        self.color = color
        self.width = Constants.BUOY_WIDTH
        self.height = Constants.BUOY_HEIGHT
        self.corners = corners
