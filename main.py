from Navigator import SimulatedNavigator

def main():
    params = {
        'boatInit': [380, 20]
    }
    navigator = SimulatedNavigator('NavChannelDemo', **params)
    navigator.run()

main()