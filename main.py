import argparse
from BuoyGenerator import generateBuoys
from Navigator import SimulatedNavigator, PixhawkNavigator
import utils

def main():
    config = parseArguments()
    if not config.pixhawk: 
        navigator = SimulatedNavigator(config)
    else:
        navigator = PixhawkNavigator(config)
    navigator.run()

def parseArguments():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('-p', '--pixhawk', action='store_true', required=False, help='Use Pixhawk')
    parser.add_argument('--task', '-t', type=str, required=True)
    parser.add_argument('--seed', '-s', type=int, required=False)
    # Parse the argument
    args = parser.parse_args()
    if args.pixhawk:
        print("RUN PIXHAWK CODE")
    if (args.seed is not None):
        config = generateBuoys(args.task, args.seed)
    else:
        config = utils.loadConfig(args.task)
    return config

main()