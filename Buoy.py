import Constants
class Buoy():
    def __init__(self, center, color):
        self.x = center[0]
        self.y = center[1]
        self.height = Constants.BUOY_HEIGHT
        self.width = Constants.BUOY_WIDTH
        self.color = color
        self.pixelData = Snapshot()
    
    def updatePixelData(self, center, width, height):
        self.pixelData.x = center[0]
        self.pixelData.y = center[1]
        self.pixelData.width = width
        self.pixelData.height = height
    
class pixelBuoy():
    def __init__(self, topLeft, width, height, color):
        self.x = topLeft[0]
        self.y = topLeft[1]
        self.width = width
        self.height = height
        self.color = color

class Snapshot():
    def __init__(self):
        self.x = None
        self.y = None
        self.width = None
        self.height = None
