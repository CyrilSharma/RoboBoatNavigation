import Constants
class Buoy():
    def __init__(self, center, color, width=None, height=None, corners=None):
        self.x = center[0]
        self.y = center[1]
        self.color = color
        if width is None:
            self.width = Constants.BUOY_WIDTH
        else:
            self.width = width
        
        if height is None:
            self.height = Constants.BUOY_HEIGHT
        else:
            self.height = height
        self.corners = corners
