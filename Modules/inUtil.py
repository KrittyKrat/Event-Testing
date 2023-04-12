import json
from Modules.events import Event

def openJson(jsonFile):
    try:
        file = open(jsonFile)
        data = json.load(file)
    except:
        print("Failed to open the command file")
        quit()

    return file, data

def readConfigFile(routerName, jsonFile):

    file, data = openJson(jsonFile)
    events = []
    connected = False

    try:
        for d in data['devices']:
            if d['router'] == routerName:
                for e in d['types']:
                    for s in e['subtypes']:
                        events.append(Event(e['type'], s['subtype'], s["trigger"], s['expected'], d['number'], data['testNumber']))
                connected = True
    except:
        print("Bad json format")
        quit()
        
    if not connected:
        print("No specified device found")
        quit()

    file.close()
    return events