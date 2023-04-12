import argparse

class cl:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def terminal(type, subtype, passedCommands, failedCommands, totalCommands, override):
    if override:
        print(f"{type:15} | {subtype:20} | {cl.OKGREEN}{passedCommands:6}{cl.ENDC} | {cl.FAIL}{failedCommands:6}{cl.ENDC} | {totalCommands:5} |", end='\r')
    else:
        print(f"{type:15} | {subtype:20} | {cl.OKGREEN}{passedCommands:6}{cl.ENDC} | {cl.FAIL}{failedCommands:6}{cl.ENDC} | {totalCommands:5} | \r")

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the router', required=True)
    parser.add_argument('--file', type=str, help='Name of the config .json file', required=True)
    parser.add_argument('--rut1', type=str, help='Main router variables (ip, username, password)', nargs=3, required=False)
    parser.add_argument('--rut2', type=str, help='Second router variables (ip, username, password)', nargs=3, required=False)
    args = parser.parse_args()
    return args