# generic configuration object
class Config():
    def __init__(self, task=None):
        self.task = task
        self.camera_width = 600  # default camera frame width
        self.camera_height = 400  # default camera frame height
