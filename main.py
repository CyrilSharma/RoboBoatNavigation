from Navigator import SimulatedNavigator

def main():
    params = {
        'boatInit': [380, 70]
    }
    navigator = SimulatedNavigator('NavChannelDemo', **params)
    navigator.run()

main()