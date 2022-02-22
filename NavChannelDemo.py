import utils
import Boat

def navigateChannel(boat, buoyList):
    closestBuoys = findClosestBuoys(buoyList)
    avgX = (closestBuoys['red'].position[0] + closestBuoys['green'].position[0]) / 2
    # figure out more about waypoints
    waypoint = [avgX, 0, 0]

# find closest buoy with specific color
def findClosestBuoys(buoyList):
    closestBuoys = {}
    for color in buoyList:
        minDist = 0
        for buoy in buoyList[color]:
            if (buoy.center[2] < minDist):
                minDist = buoy.center[2]
                closestBuoys[color] = buoy
    return closestBuoys
