import tkinter
import FrameConstants as FC
import time
import utils

class Visualizer():
    def __init__(self, boat, buoys):
        self.initialize(buoys, boat)

    def initialize(self, buoys, boat):
        self.Window = tkinter.Tk()
        self.Window.geometry(f'{FC.Window_Width}x{FC.Window_Height}')
        self.canvas = tkinter.Canvas(self.Window)
        self.canvas.configure(bg="Blue")
        self.canvas.pack(fill="both", expand=True)
        self.makeBuoys(buoys)
        self.boat = self.canvas.create_rectangle(boat.x - boat.width / 2, boat.y - boat.width / 2, boat.x + boat.width / 2, boat.y + boat.width / 2, fill=boat.color)
    
    def makeBuoys(self, buoys):
        for buoy in buoys:
            self.canvas.create_rectangle(buoy.x - buoy.width / 2, buoy.y - buoy.width / 2, buoy.x + buoy.width / 2, buoy.y + buoy.width / 2, fill=buoy.color)
    
    def animate(self, update):
        self.canvas.move(self.boat, update[0], update[1])
        self.Window.update()
 
def test():
    vis = Visualizer(utils.getBuoysAbs('NavChannelDemo'))
    while True:
        vis.animate([0,10])
        time.sleep(FC.Refresh_Sec)

if __name__ == "__main__":
    test()