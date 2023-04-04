from datetime import datetime
import csv

def writeToCSV(events, routerName):
    tempName = routerName + "_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ".csv"
    fileName = "Results/" + tempName
    fileName = "Results/test.csv"
    
    try:
        file = open(fileName, 'w')
        writer = csv.writer(file)
    except:
        print("Failed to open file")
        quit()
    
    try:
        writer.writerow(["Event", "Gotten", "Expected", "Number Got", "Number Sent", "Passed"])

        for i in range(0, len(events)):
            writer.writerow([events[i].subtype, events[i].gotten, events[i].expected, events[i].nrGotten, events[i].nrExpected, events[i].success])
    except:
        print("Failed to write to .csv file")
        quit()
    
    file.close()
    return tempName