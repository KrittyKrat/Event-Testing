import requests
import time
import paramiko
import random
from datetime import datetime, timedelta
from Modules import terminal

def executeCommand(sc, command):
    try:
        stdin,stdout,stderr = sc.exec_command(command, timeout=1)
        return stdout
    except:
        print("\nConnection to ssh lost, retrying...", end='\r')
        quit()

def getToken(webLogin, url):
    if url == None:
        api_url = "http://192.168.1.1/api/login"
    else:
        api_url = url

    if webLogin == None:
        login = {"username":"admin", "password":"Admin123"}
    else:
        login = {"username":webLogin[0], "password":webLogin[1]}

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
                "telnum":"+447342780080",
                "event":event.type,
                "message":event.subtype + " - " + str(datetime.now()),
                "recipient_format":"single",
                "eventMark":event.subtype,
                "id":"cfg0392bd",
                "recipEmail":["thejjjane@gmail.com"]},
                "emailgroup":"sender"}
    return body

def createTemp(header, event):
    post = True
    match event.subtype:
        case "ddns":
            body = {"data":{"id":str(random.randrange(9999))}}
        case "dmvpn":
            body = {"data":{"id":str(random.randrange(9999))}}
        case "openvpn":
            body = {"data":{"id":str(random.randrange(9999)),"type":"client"}}
        case "gps":
            body = {"data":{"enabled":"1",".type":"section","glonass_sup":"0","id":"general","beidou_sup":"0","galileo_sup":"0"}}
            post = False
        case "fstab":
            body = {"data":{"id":"general",".type":"global","auto_sync":"1"}}
            post = False
        case "hostblock":
            body = {"data":{"enabled":"1",".type":"hostblock","id":"general","mode":"whitelist"}}
            post = False
        case "call_utils":
            body = {"data":{"id":"general",".type":"call","action":"ignore","line_close_time":""}}
            post = False
        case "blesem":
            body = {"data":{"enabled":"1",".type":"section","id":"general"}}
            post = False
        case "firewall":
            body = {"data":{"drop_invalid":"1",".type":"defaults","auto_helper":"1","input":"REJECT","forward":"REJECT","id":"general","output":"ACCEPT"}}
            post = False
        case "chilli":
            temp = requests.get(event.trigger, headers=header)
            tempId = temp.json()['data'][0]['id']
            event.trigger = event.trigger + "/" + tempId
            body = {"data":{".type":"group","id":tempId,"defidletimeout":"1","day":"2","period":"3","downloadbandwidth":"","uploadbandwidth":"","downloadlimit":"","uploadlimit":"","defsessiontimeout":"","warning":""}}
            post = False
        case other:
            body = {"data":{}}

    api_url = event.trigger

    if post:
        response = requests.post(api_url, headers=header, json=body)
    else:
        response = requests.put(api_url, headers=header, json=body)
        
    return response.json()['data']['id']

def deleteTemp(header, event, id):
    delete = False
    match event.subtype:
        case "call_utils":
            body = {"data":{"id":"general",".type":"call","action":"reject","line_close_time":""}}
        case "blesem":
            body = {"data":{"enabled":"0",".type":"section","id":"general"}}
        case "firewall":
            body = {"data":{"drop_invalid":"0",".type":"defaults","auto_helper":"1","input":"REJECT","forward":"REJECT","id":"general","output":"ACCEPT"}}
        case "chilli":
            body = {"data":{".type":"group","id":id,"defidletimeout":"1","day":"1","period":"3","downloadbandwidth":"","uploadbandwidth":"","downloadlimit":"","uploadlimit":"","defsessiontimeout":"","warning":""}}
        case "fstab":
            body = {"data":{"id":"general",".type":"global","auto_sync":"0"}}
        case "gps":
            body = {"data":{"enabled":"0",".type":"section","glonass_sup":"0","id":"general","beidou_sup":"0","galileo_sup":"0"}}
        case "hostblock":
            body = {"data":{"enabled":"0",".type":"hostblock","id":"general","mode":"whitelist"}}
        case other:
            body = {"data":[id]}
            delete = True

    api_url = event.trigger

    if delete:
        response = requests.delete(api_url, headers=header, json=body)
    else:
        response = requests.put(api_url, headers=header, json=body)

def findEvent(e, header, api_url, header2):
    ssh = connectSSH(None)
    ids = prepFailover(header)
    match e.type:
        case "Config":
            testConfig(e, header, api_url)
        case "SSH":
            testSSH(e, header, api_url)
        case "Web UI":
            testWeb(e, header, api_url)
        case "Mobile Data":
            testMobData(e, header, api_url)
        case "SIM switch":
            testSimSwitch(e, header, api_url)
        case "Failover":
            testFailover(e, header, api_url, ids)
        case "Switch Events":
            testPorts(e, header, api_url)
        case "Reboot":
            testReboot(e, header, api_url)
        case "SMS":
            testSMS(e, header, api_url)
        case "Switch Topology":
            testTopology(e, header, api_url)
        case "WiFi":
            testWiFi(e, header, api_url, header2)
        case "DHCP":
            testDHCP(e, header, api_url, header2)

def toggleVlan(on, header):
    vlan_url = "http://192.168.1.1/api/network/vlan/port_based/config"
    if on:
        body = {"data": [{"lan1": "u","lan2": "u","lan3": "u","id": "cfg081ec7"}]}
    else:
        body = {"data": [{"lan1": "u","lan2": "","lan3": "","id": "cfg081ec7"}]}
    requests.put(vlan_url, headers=header, json=body)
    time.sleep(5)

def testDHCP(e, header, api_url, header2):
    trig = e.trigger.split() 
    dhcp_url = "http://192.168.1.1/api/network/dhcp/servers/config/lan"
    bodyChange = {"data": {"end_ip": "192.168.1."+trig[3],"start_ip": "192.168.1."+trig[2],"leasetime": "10h"}}
    bodyOG = {"data": {"end_ip": "192.168.1."+trig[1],"start_ip": "192.168.1."+trig[0]},"leasetime": "10h"}

    bodyUpdate = {"data": {".type": "interface","fwzone": "lan","id": "lan","ip6assign": "60","ifname": ["eth0"],"proto": "static"}}
    update_url = "http://192.168.1.1/api/network/interfaces/config/lan"

    response = changeEventConfig(e, header, api_url)
    if e.subtype == "lan":
        requests.put(dhcp_url, headers=header, json=bodyChange)
        time.sleep(5)
        requests.put(update_url, headers=header, json=bodyUpdate)
        time.sleep(30)
        requests.put(dhcp_url, headers=header, json=bodyOG)
        time.sleep(5)
        requests.put(update_url, headers=header, json=bodyUpdate)
        time.sleep(30)

    if e.subtype == "wifi":
        body = {"data":{"bssid":trig[0],"ssid":trig[1],"password":trig[2],"network":trig[3],"fwzone":"wan","device":"radio0"}}
        wifi_url = "http://192.168.1.2/api/network/wireless/devices/actions/join_wifi_network"
        requests.post(wifi_url, headers=header2, json=body)
        time.sleep(60)
        body = {"data":[trig[3]]}
        wifi_url = "http://192.168.1.2/api/network/interfaces/config"
        aaa = requests.delete(wifi_url, headers=header2, json=body)

def testWiFi(e, header, api_url, header2):
    response = changeEventConfig(e, header, api_url)

    trig = e.trigger.split() 
    if e.subtype == "client connected":
        body = {"data":{"bssid":trig[0],"ssid":trig[1],"password":trig[2],"network":trig[3],"fwzone":"wan","device":"radio0"}}
        wifi_url = "http://192.168.1.2/api/network/wireless/devices/actions/join_wifi_network"
        z = requests.post(wifi_url, headers=header2, json=body)
    elif e.subtype == "client disconnected":
        body = {"data":[trig[0]]}
        wifi_url = "http://192.168.1.2/api/network/interfaces/config"
        z = requests.delete(wifi_url, headers=header2, json=body)

    time.sleep(10)

def testTopology(e, header, api_url):
    bodyOff = {"data": [{"enabled": "0","id": "wan",".type": "interface","metric": "1"}]}
    bodyOn = {"data": [{"enabled": "1","id": "wan",".type": "interface","metric": "1"}]}
    requests.put(e.trigger, headers=header, json=bodyOff)
    time.sleep(5)
    response = changeEventConfig(e, header, api_url)
    requests.put(e.trigger, headers=header, json=bodyOn)
    time.sleep(10)

def testReboot(e, header, api_url):

    response = changeEventConfig(e, header, api_url)
    time.sleep(3)

    match e.subtype:
        case "ping reboot":
            rez = requests.post(e.trigger, headers=header, json={"data":{}})
            tempId = rez.json()['data']['id']
            body = {"data":{".type":"ping_reboot","retry":"1","id":tempId,"ip_type":"ipv4","packet_size":"56","time_out":"1","enable":"1","type":"ping","action":"1","time":"5","host":"192.168.55.55","stop_action":"0","number":"","interface":"1"}}
            rez = requests.put(e.trigger + "/" + tempId, headers=header, json=body)
            time.sleep(480)
            header = {"Authorization": "Bearer " + getToken(None, None)}
            requests.delete(e.trigger, headers=header, json={"data":[tempId]})
        case "reboot scheduler":
            dt = datetime.now() + timedelta(seconds=60)
            rez = requests.post(e.trigger, headers=header, json={"data":{}})
            tempId = rez.json()['data']['id']
            body = {"data":{"id":tempId,".type":"reboot_instance","action":"1","period":"week","days":["mon","tue","wed","thu","fri","sat","sun"],"time":[dt.strftime("%H:%M")],"months":"","month_day":"","enable":"1","force_last":""}}
            rez = requests.put(e.trigger + "/" + tempId, headers=header, json=body)
            time.sleep(180)
            header = {"Authorization": "Bearer " + getToken(None, None)}
            requests.delete(e.trigger, headers=header, json={"data":[tempId]})
        case "web ui":
            rez = requests.post(e.trigger, headers=header)
        case "sms reboot":
            body = {"data":{"modem":"3-1","number":e.nrExpected,"message": e.trigger}}
            msg_url = "http://192.168.1.1/api/services/mobile_utilities/sms_messages/send/actions/send"
            rez = requests.post(msg_url, headers=header, json=body)
    time.sleep(120)

def testPorts(e, header, api_url):
    prep = requests.get("http://192.168.1.1/api/services/port_mirroring/config/general", headers=header)
    if prep.json()['data']['mirror_monitor_port'] == "disabled":
        temp = "1"
    else: 
        temp = "disabled"

    response = changeEventConfig(e, header, api_url)
    time.sleep(3)
    requests.put(e.trigger, headers=header, json={"data":{"id":"general",".type":"switch","mirror_monitor_port":temp,"mirror_source_port":"","enable_mirror_rx":"","enable_mirror_tx":""}})
    time.sleep(3)

def prepFailover(header):
    get_url = "http://192.168.1.1/api/network/mwan3/general/status"
    res = requests.get(get_url, headers=header)
    ids = []
    for id in res.json()['data']:
        ids.append(id)
        put_url = "http://192.168.1.1/api/network/mwan3/interfaces/config/" + id
        body = {"data":{"enabled":"1",".type":"interface","track_ip":["1.1.1.1","8.8.8.8"],"up":"3","reliability":"1","id":id,"count":"1","track_method":"ping","interval":"3","down":"3","flush_conntrack":""}}
        requests.put(put_url, headers=header, json=body)
    return ids

def testFailover(e, header, api_url, ids):
    get_url = "http://192.168.1.1/api/bulk"
    mainOn = {"data":[{"method": "PUT","endpoint": "/api/network/interfaces/config","data": [{"enabled": "1",".type": "interface","id": ids[0],"metric": "2"}],"awaitNetwork": False}]}
    mainOff = body = {"data":[{"method": "PUT","endpoint": "/api/network/interfaces/config","data": [{"enabled": "0",".type": "interface","id": ids[0],"metric": "2"}],"awaitNetwork": False}]}
    
    if e.trigger == "1": 
        res = requests.post(get_url, headers=header, json=mainOff)
        time.sleep(20)
    else:
        requests.post(get_url, headers=header, json=mainOn)
        time.sleep(20)
    
    response = changeEventConfig(e, header, api_url)

    if e.trigger == "1": 
        requests.post(get_url, headers=header, json=mainOn)
        time.sleep(20)
    else:
        requests.post(get_url, headers=header, json=mainOff)
        time.sleep(20)

    requests.post(get_url, headers=header, json=mainOn)

def testSimSwitch(e, header, api_url):
    response = changeEventConfig(e, header, api_url)

    if e.subtype == "to SIM1":
        sim_url = "http://192.168.1.1/api/network/mobile/simcards/config/cfg02aa0e"
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg02aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        sim_url2 = "http://192.168.1.1/api/network/mobile/sim_switch/config/cfg02aa0e"
        body2 = {"data":{"enabled":"1",".type":"sim","id":"cfg02aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}
    elif e.subtype == "to SIM2":
        sim_url = "http://192.168.1.1/api/network/mobile/simcards/config/cfg01aa0e"
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg01aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        sim_url2 = "http://192.168.1.1/api/network/mobile/sim_switch/config/cfg01aa0e"
        body2 = {"data":{"enabled":"1",".type":"sim","id":"cfg01aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}
    
    requests.put(sim_url, headers=header, json=body)
    time.sleep(10)
    requests.put(sim_url2, headers=header, json=body2)
    time.sleep(70)

    if e.subtype == "to SIM1":
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg02aa0e","primary":"0","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        body2 = {"data":{"enabled":"0",".type":"sim","id":"cfg02aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}
    elif e.subtype == "to SIM2":
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg01aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        body2 = {"data":{"enabled":"0",".type":"sim","id":"cfg01aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}

    requests.put(sim_url2, headers=header, json=body2)
    time.sleep(5)
    requests.put(sim_url, headers=header, json=body)
    time.sleep(30)

def testSMS(e, header, api_url):
    response = changeEventConfig(e, header, api_url)

    body = {"data":{"modem":"3-1","number":e.nrExpected,"message": e.trigger}}
    msg_url = "http://192.168.1.1/api/services/mobile_utilities/sms_messages/send/actions/send"

    r = requests.post(msg_url, headers=header, json=body)
    time.sleep(3)

def testMobData(e, header, api_url):
    trig = e.trigger.split()
    dataOn = {"data":{"modem":"3-1","number":e.nrExpected,"message": trig[0] + " mobileon"}}
    dataOff = {"data":{"modem":"3-1","number":e.nrExpected,"message": trig[0] + " mobileoff"}}
    msg_url = "http://192.168.1.1/api/services/mobile_utilities/sms_messages/send/actions/send"

    if trig[1] == "mobileon":
        requests.post(msg_url, headers=header, json=dataOff)
        time.sleep(2)
    else:
        requests.post(msg_url, headers=header, json=dataOn)
        time.sleep(80)

    response = changeEventConfig(e, header, api_url)

    if trig[1] == "mobileon":
        requests.post(msg_url, headers=header, json=dataOn)
    else:
        requests.post(msg_url, headers=header, json=dataOff)
        time.sleep(2)

    requests.post(msg_url, headers=header, json=dataOn)

def testWeb(e, header, api_url):
    response = changeEventConfig(e, header, api_url)
    getToken(e.trigger.split(), None)

def testSSH(e, header, api_url):
    response = changeEventConfig(e, header, api_url)
    ssh = connectSSH(e.trigger.split())
    ssh.close()

def testConfig(e, header, api_url):
    id = createTemp(header, e)
    time.sleep(5)
    response = changeEventConfig(e, header, api_url)
    deleteTemp(header, e, id)

def changeEventConfig(e, header, api_url):
    body = getBody(e)
    response = requests.put(api_url, headers=header, json=body)
    time.sleep(8)
    return response

def testAll(events):
    token = getToken(None, None)
    header = {"Authorization": "Bearer " + token}

    token2 = getToken(None, "http://192.168.1.2/api/login")
    header2 = {"Authorization": "Bearer " + token2}
    
    api_url = "http://192.168.1.1/api/services/events_reporting/config/cfg0192bd"

    totalCommands = len(events)
    passedCommands = 0
    failedCommands = 0

    terminal.terminal("Type", "Subtype", "Passed", "Failed", "Total", False)

    for e in events:
        findEvent(e, header, api_url, header2)
        terminal.terminal(e.type, e.subtype, "", "", totalCommands, False)
        #response.json()['success']

        if e.type == "Reboot":
            token = getToken(None, None)
            header = {"Authorization": "Bearer " + token}