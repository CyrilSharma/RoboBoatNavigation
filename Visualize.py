import tkinter
import FrameConstants as FC
import time
import utils

class Visualizer():
    def __init__(self):
        self.Window = tkinter.Tk()
        self.Window.bind('<Escape>', lambda e: self.Window.destroy())
        self.Window.geometry(f'{FC.Window_Width}x{FC.Window_Height}')
        self.canvas = tkinter.Canvas(self.Window)
        self.canvas.configure(bg="Blue")
        self.canvas.pack(fill="both", expand=True)

class TopDownVisualizer(Visualizer):
    def __init__(self, boat, buoys):
        super().__init__()
        self.initialize(buoys, boat)

    def initialize(self, buoys, boat):
        self.makeBuoys(buoys)
        self.boat = self.canvas.create_rectangle(boat.x - boat.width / 2, boat.y - boat.width / 2, boat.x + boat.width / 2, boat.y + boat.width / 2, fill=boat.color)
    
    def makeBuoys(self, buoys):
        for buoy in buoys:
            self.canvas.create_rectangle(buoy.x - buoy.width / 2, buoy.y - buoy.width / 2, buoy.x + buoy.width / 2, buoy.y + buoy.width / 2, fill=buoy.color)
    
    def animate(self, update):
        self.canvas.move(self.boat, update[0], update[1])
        self.Window.update()

class CameraVisualizer(Visualizer):
    def __init__(self, buoys):
        super().__init__()
        self.makeBuoys(buoys)
    
    def makeBuoys(self, buoys):
        for buoy in buoys:
            self.canvas.create_rectangle(buoy.x - buoy.width / 2, FC.Window_Height - (buoy.y - buoy.height / 2), buoy.x + buoy.width / 2, FC.Window_Height - (buoy.y + buoy.height / 2), fill=buoy.color)
    
    def update(self, buoys):
        self.canvas.delete('all')
        self.makeBuoys(buoys)
        self.Window.update()