from Modules import terminal
from Modules import inUtil
from Modules import outUtil
from Modules import test

def main():
    args = terminal.arguments()
    routerName =  args.name.upper()
    jsonFile = args.file
    sshVar = args.ssh
    modVar = args.mod

    events = inUtil.readConfigFile(routerName, jsonFile)
    outUtil.writeToCSV(events, routerName)
    print("Router being tested: " + routerName)
    test.testAll(events)

if __name__ == "__main__":
    main()