import argparse
from Config import Config
from Navigator import SimulatedNavigator
import utils

def main():
    params = {
        'boatInit': [380, 20]
    }

    navigator = SimulatedNavigator('NavChannelDemo', **params)
    navigator.run()

def parseArguments():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--task', type=str, required=True)
    parser.add_argument('--randomBuoys', type=bool, required=False)
    parser.add_argument('--seed', type=int, required=False)
    # Parse the argument
    args = parser.parse_args()
    return 

main()