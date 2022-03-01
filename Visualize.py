import tkinter
import FrameConstants as FC
import time
import utils

class Visualizer():
    def __init__(self, buoys):
        self.initialize()
        self.makeBuoys(buoys)
        pass

    def initialize(self):
        self.Window = tkinter.Tk()
        self.Window.title("Python Guides")
        self.Window.geometry(f'{FC.Window_Width}x{FC.Window_Height}')
        self.canvas = tkinter.Canvas(self.Window)
        self.canvas.configure(bg="Blue")
        self.canvas.pack(fill="both", expand=True)
        self.boat = self.canvas.create_rectangle(50,50,60,100,fill="Red", outline="Red", width=4)
    
    def makeBuoys(self, buoys):
        print(buoys)
        for color in buoys:
            print(color)
            print(buoys[color])
            for buoy in buoys[color]:
                print(buoy)
                self.canvas.create_rectangle(buoy.corners[0][0], buoy.corners[0][1], buoy.corners[1][0], buoy.corners[1][1], fill=color, outline=color, width=4)
    
    def animate(self, velocity):
        self.canvas.move(self.boat, velocity[0] * FC.Refresh_Sec, velocity[1] * FC.Refresh_Sec)
        self.Window.update()
 
def main():
    vis = Visualizer(utils.getBuoysAbs('NavChannelDemo'))
    while True:
        vis.animate([10,10])
        time.sleep(FC.Refresh_Sec)

if __name__ == "__main__":
    main()