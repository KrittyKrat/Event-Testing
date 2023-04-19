from Modules import terminal_utility
from Modules import read_file_utility
from Modules import print_file_utility
from Modules import test_all

def main():
    args = terminal_utility.arguments()
    routerName =  args.name.upper()
    jsonFile = args.file
    rut1 = args.rut1
    rut2 = args.rut2
    mod = args.mod

    events = read_file_utility.readConfigFile(routerName, jsonFile)
    print("Router being tested: " + routerName)
    test_all.testAll(events, rut1, rut2, mod)
    print_file_utility.writeToCSV(events, routerName)

if __name__ == "__main__":
    main()