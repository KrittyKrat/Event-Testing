from Modules import terminal
from Modules import inUtil
from Modules import outUtil
from Modules import test

def main():
    args = terminal.arguments()
    routerName =  args.name.upper()
    jsonFile = args.file
    rut1 = args.rut1
    rut2 = args.rut2
    modVar = args.mod

    events = inUtil.readConfigFile(routerName, jsonFile)
    print("Router being tested: " + routerName)
    test.testAll(events, rut1, rut2)
    outUtil.writeToCSV(events, routerName)

if __name__ == "__main__":
    main()