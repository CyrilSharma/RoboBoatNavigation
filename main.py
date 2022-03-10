import argparse
from BuoyGenerator import generateBuoys
from Navigator import SimulatedNavigator
import utils

def main():
    config = parseArguments()
    navigator = SimulatedNavigator(config)
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
    if (args.randomBuoys):
        config = generateBuoys(args.task, args.seed)
    else:
        config = utils.loadConfig(args.task)
    return generateBuoys(args.task, args.randomBuoys, args.seed)

main()