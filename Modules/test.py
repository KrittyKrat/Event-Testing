import requests
import time
import paramiko
import random
from datetime import datetime, timedelta
from Modules import terminal
from Modules import testSpecific

def executeCommand(sc, command):
    try:
        stdin,stdout,stderr = sc.exec_command(command, timeout=1)
        return stdout
    except:
        print("\nConnection to ssh lost, retrying...", end='\r')
        quit()

def getToken(rut, ip):

    api_url = "http://"+ip+"/api/login"

    if rut == None:
        login = {"username":"admin", "password":"Admin123"}
    else:
        login = {"username":rut[1], "password":rut[2]}

    response = requests.post(api_url, json=login)
    try:
        token = response.json()['ubus_rpc_session']
    except:
        token = None

    try:
        token = response.json()['jwtToken']
    except:
        pass

    return token

def connectSSH(sshVar):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if sshVar == None:
            ssh_client.connect(hostname='192.168.1.1',username='root',password='Admin123', timeout=5)
        else:
            ssh_client.connect(hostname=sshVar[0],username=sshVar[1],password=sshVar[2], timeout=5)
    except:
        pass
    
    return ssh_client

def getBody(event):
    body = {"data":{".type":"rule",
                "action":"sendEmail",
                "enable":"1",
                "telnum":event.testNumber,
                "event":event.type,
                "message":event.subtype + " - " + str(datetime.now()),
                "recipient_format":"single",
                "eventMark":event.subtype,
                "id":"cfg0392bd",
                "recipEmail":["thejjjane@gmail.com"]},
                "emailgroup":"sender"}

    body = {"data": {
                ".type": "rule",
                "action": "sendSMS",
                "enable": "1",
                "telnum": event.testNumber,
                "event": event.type,
                "id": "cfg0392bd",
                "message": event.expected,
                "subject": "",
                "recipient_format": "single",
                "recipEmail": "",
                "emailgroup": "",
                "eventMark": event.subtype
            }
        }
    return body

def findEvent(e, header, api_url, header2, rut1):
    #ssh = connectSSH(None)
    match e.type:
        case "Config":
            testSpecific.testConfig(e, header, api_url)
        case "SSH":
            testSpecific.testSSH(e, header, api_url)
        case "Web UI":
            testSpecific.testWeb(e, header, api_url)
        case "Mobile Data":
            testSpecific.testMobData(e, header, api_url)
        case "SIM switch":
            testSpecific.testSimSwitch(e, header, api_url)
        case "Failover":
            ids = prepFailover(header)
            testSpecific.testFailover(e, header, api_url, ids)
        case "Switch Events":
            testSpecific.testPorts(e, header, api_url)
        case "Reboot":
            testSpecific.testReboot(e, header, header2, api_url, rut1)
        case "SMS":
            testSpecific.testSMS(e, header, api_url)
        case "Switch Topology":
            testSpecific.testTopology(e, header, api_url)
        case "WiFi":
            testSpecific.testWiFi(e, header, api_url, header2)
        case "DHCP":
            testSpecific.testDHCP(e, header, api_url, header2)

def toggleVlan(on, header):
    vlan_url = "http://"+IP1+"/api/network/vlan/port_based/config"
    if on:
        body = {"data": [{"lan1": "u","lan2": "u","lan3": "u","id": "cfg081ec7"}]}
    else:
        body = {"data": [{"lan1": "u","lan2": "","lan3": "","id": "cfg081ec7"}]}
    requests.put(vlan_url, headers=header, json=body)
    time.sleep(5)

def prepFailover(header):
    get_url = "http://"+IP1+"/api/network/mwan3/general/status"
    res = requests.get(get_url, headers=header)
    ids = []
    for id in res.json()['data']:
        ids.append(id)
        put_url = "http://"+IP1+"/api/network/mwan3/interfaces/config/" + id
        body = {"data":{"enabled":"1",".type":"interface","track_ip":["1.1.1.1","8.8.8.8"],"up":"3","reliability":"1","id":id,"count":"1","track_method":"ping","interval":"3","down":"3","flush_conntrack":""}}
        requests.put(put_url, headers=header, json=body)
    return ids

def changeEventConfig(e, header, api_url):
    body = getBody(e)
    response = requests.put(api_url, headers=header, json=body)
    time.sleep(8)
    return response

def setGlobalVariables(rut1, rut2):
    global IP1
    global IP2
    if rut1 == None:
        IP1 = "192.168.1.1"
    else:
        IP1 = rut1[0]

    if rut2 == None:
        IP2 = "192.168.1.2"
    else:
        IP2 = rut2[0]

def testAll(events, rut1, rut2):

    setGlobalVariables(rut1, rut2)
    testSpecific.setGlobalIP(IP1, IP2)
    
    token = getToken(rut1, IP1)
    header = {"Authorization": "Bearer " + token}

    token2 = getToken(rut2, IP2)
    header2 = {"Authorization": "Bearer " + token2}
    
    api_url = "http://"+IP1+"/api/services/events_reporting/config/cfg0192bd"

    totalCommands = len(events)
    passedCommands = 0
    failedCommands = 0

    setupSMS(header2)

    terminal.terminal("Type", "Subtype", "Passed", "Failed", "Total", False)

    timeout = 5
    i=0
    while i < len(events):
        try:
            terminal.terminal(events[i].type, events[i].subtype, passedCommands, failedCommands, totalCommands, False)
            findEvent(events[i], header, api_url, header2, rut1)

            if events[i].type == "Reboot":
                token = getToken(rut1, IP1)
                header = {"Authorization": "Bearer " + token}
                token2 = getToken(rut2, IP2)
                header2 = {"Authorization": "Bearer " + token2}

            checkSMS(events[i], header2)
            passedCommands, failedCommands = checkGotten(events[i], passedCommands, failedCommands)
            timeout = 3
            i += 1
        except:
            if timeout > 0:
                timeout = timeout - 1
            else:
                print("No connection found, retrying...")
                quit()
            print("Lost connection rip")
            time.sleep(10)

    terminal.terminal("---", "---", passedCommands, failedCommands, totalCommands, False)

def setupSMS(header2):
    get_url = "http://"+IP2+"/api/services/mobile_utilities/sms_messages/read/config"
    del_ulr = "http://"+IP2+"/api/services/mobile_utilities/sms_messages/read/config/1-1.4"

    response = requests.get(get_url, headers=header2)
    nr = []

    for i in response.json()['data']:
        nr.append(i['id'])

    #if len(response.json()['data']) > 5:
    #    nr = ["2", "3", "1", "0", str(len(response.json()['data']) - 1)]
    #else:
    #    for d in reversed(range(0, len(response.json()['data']))):
    #        nr.append(str(d))

    body = {"data":nr}
    rz = requests.delete(del_ulr, headers=header2, json=body)

def checkSMS(e, header2):
    get_url = "http://"+IP2+"/api/services/mobile_utilities/sms_messages/read/config"
    timeout = 8
    temp = ""
    tempNr = ""

    for i in range(0, timeout):
        response = requests.get(get_url, headers=header2)
        #print(response.text)
        for d in response.json()['data']:
            if(d['message'] == e.expected):
                e.gotten = e.expected
                e.nrGotten = e.nrExpected
                setupSMS(header2)
                return
            else:
                temp = d['message']
                tempNr = d['sender']

        setupSMS(header2)
        time.sleep(1.5)

    e.gotten  = temp
    e.nrGotten = tempNr

def checkGotten(e, passedCommands, failedCommands):
    if e.gotten == e.expected and e.nrGotten == e.nrExpected:
        e.success = "Pass"
        passedCommands = passedCommands + 1
    else:
        e.success = "Fail"
        failedCommands = failedCommands + 1
    return passedCommands, failedCommands