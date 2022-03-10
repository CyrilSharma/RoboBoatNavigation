import tkinter
import FrameConstants as FC

class Visualizer():
    def __init__(self):
        self.Window = tkinter.Tk()
        self.Window.bind('<Escape>', lambda e: self.Window.destroy())
        self.Window.geometry(f'{FC.Window_Width}x{FC.Window_Height}')
        self.canvas = tkinter.Canvas(self.Window)
        self.canvas.configure(bg="Blue")
        self.canvas.pack(fill="both", expand=True)

class TopDownVisualizer(Visualizer):
    def __init__(self, bouys, boat):
        super().__init__()
        self.boat = self.canvas.create_rectangle(boat.x - boat.width / 2, boat.y - boat.width / 2, boat.x + boat.width / 2, boat.y + boat.width / 2, fill=boat.color)
        self.makeBuoys(bouys)
    
    def makeBuoys(self, buoys):
        for buoy in buoys:
            self.canvas.create_rectangle(buoy.x - buoy.width / 2, buoy.y - buoy.width / 2, buoy.x + buoy.width / 2, buoy.y + buoy.width / 2, fill=buoy.color)
    
    def animate(self, update):
        self.canvas.move(self.boat, update[0], update[1])
        self.Window.update()

class CameraVisualizer(Visualizer):
    def __init__(self):
        super().__init__()
    
    def makeBuoys(self, buoys, boat):
        sortedBuoys = sorted(buoys, key=lambda buoy: (buoy.x - boat.x) ** 2 + (buoy.y - boat.y) ** 2, reverse=True)
        for buoy in sortedBuoys:
            pix = buoy.pixelData
            self.canvas.create_rectangle(pix.x - pix.width / 2, FC.Window_Height - (pix.y - pix.height / 2), pix.x + pix.width / 2, FC.Window_Height - (pix.y + pix.height / 2), fill=buoy.color)
    
    def update(self, buoys, boat):
        self.canvas.delete('all')
        self.makeBuoys(buoys, boat)
        self.Window.update()