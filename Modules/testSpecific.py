import requests
import random
import time
from datetime import datetime, timedelta
from Modules import test

def setGlobalIP(i1, i2):
    global IP1
    global IP2
    IP1 = i1
    IP2 = i2

def testConfig(e, header, api_url):
    id = createTemp(header, e)
    time.sleep(5)
    response = test.changeEventConfig(e, header, api_url)
    deleteTemp(header, e, id)
    time.sleep(2)

def createTemp(header, event):
    post = False
    match event.subtype:
        case "ddns":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "dmvpn":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "ipsec":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "openvpn":
            body = {"data":{"id":str(random.randrange(9999)),"type":"client"}}
            post = True
        case "network":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "vrrpd":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "profiles":
            body = {"data":{"id":str(random.randrange(9999)),"from_current_profile":"0",".type":"profile"}}
            post = True
        case "gps":
            body = {"data":{"enabled":"1",".type":"section","glonass_sup":"0","id":"general","beidou_sup":"0","galileo_sup":"0"}}
        case "fstab":
            body = {"data":{"id":"general",".type":"global","auto_sync":"1"}}
        case "hostblock":
            body = {"data":{"enabled":"1",".type":"hostblock","id":"general","mode":"blacklist"}}
        case "call_utils":
            body = {"data":{"id":"general",".type":"call","action":"ignore","line_close_time":""}}
        case "blesem":
            body = {"data":{"enabled":"1",".type":"section","id":"general"}}
        case "firewall":
            body = {"data":{"drop_invalid":"1",".type":"defaults","auto_helper":"1","input":"REJECT","forward":"REJECT","id":"general","output":"ACCEPT"}}
        case "iojuggler":
            body = {"data":{"enabled":"1",".type":"general","id":"general"}}
        case "ioman":
            body = {"data":{"enabled":"1",".type":"scheduler_general","id":"general"}}
        case "dropbear":
            body = {"data":{".type":"dropbear","id":"general","port":"111","_sshWanAccess":"0","enable":"1","enable_key_ssh":"0"}}
        case "ulog":
            body = {"data":{"enabled":"0",".type":"ulogd","network":["lan"],"id":"general"}}
        case "mosquitto":
            body = {"data":{"enabled":"1","max_queued_messages":"1000","local_port":["1883"],"max_packet_size":"1048576","anonymous_access":"1","persistence":"0","use_tls_ssl":"0","enable_ra":"0","id":"general",".type":"mqtt","acl_file_path":"","password_file":""}}
        case "mqtt_pub":
            body = {"data":{"id":"general",".type":"mqtt_pub","enabled":"1","remote_addr":"www.test.com","remote_port":"1883","username":"","password":"","tls":"0"}}
        case "wireless":
            body = {"data":{"noscan":"0",".type":"wifi-device","country":"US","id":"radio0","legacy_rates":"1","hwmode":"n","txpower":"23","channel":"auto","htmode":"HT20","enabled":"0","distance":"","frag":"","rts":"","beacon_int":""}}
        case "upnpd":
            body = {"data":{"enabled":"1","log_output":"0","upload":"512","system_uptime":"1","uuid":"","serial_number":"","model_number":"","notify_interval":"","clean_ruleset_threshold":"","clean_ruleset_interval":"","presentation_url":""}}
        case "chilli":
            temp = requests.get(event.trigger, headers=header)
            tempId = temp.json()['data'][0]['id']
            event.trigger = event.trigger + "/" + tempId
            body = {"data":{".type":"group","id":tempId,"defidletimeout":"1","day":"2","period":"3","downloadbandwidth":"","uploadbandwidth":"","downloadlimit":"","uploadlimit":"","defsessiontimeout":"","warning":""}}
        case other:
            body = {"data":{}}
            post = True

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
            body = {"data":{"enabled":"0",".type":"hostblock","id":"general","mode":"blacklist"}}
        case "iojuggler":
            body = {"data":{"enabled":"0",".type":"general","id":"general"}}
        case "ioman":
            body = {"data":{"enabled":"0",".type":"scheduler_general","id":"general"}}
        case "dropbear":
            body = {"data":{".type":"dropbear","id":"general","port":"22","_sshWanAccess":"0","enable":"1","enable_key_ssh":"0"}}
        case "ulog":
            body = {"data":{"enabled":"1",".type":"ulogd","network":["lan"],"id":"general"}}
        case "mqtt_pub":
            body = {"data":{"id":"general",".type":"mqtt_pub","enabled":"0","remote_addr":"","remote_port":"1883","username":"","password":"","tls":"0"}}
        case "mosquitto":
            body = {"data":{"enabled":"0","max_queued_messages":"1000","local_port":["1883"],"max_packet_size":"1048576","anonymous_access":"1","persistence":"0","use_tls_ssl":"0","enable_ra":"0","id":"general",".type":"mqtt","acl_file_path":"","password_file":""}}
        case "wireless":
            body = {"data":{"noscan":"0",".type":"wifi-device","country":"US","id":"radio0","legacy_rates":"1","hwmode":"n","txpower":"23","channel":"auto","htmode":"HT20","enabled":"1","distance":"","frag":"","rts":"","beacon_int":""}}
        case "upnpd":
            body = {"data":{"secure_mode":"1",".type":"upnpd","upnp_lease_file":"/var/run/miniupnpd.leases","download":"1024","port":"5000","id":"general","enabled":"0","log_output":"0","upload":"512","system_uptime":"1","uuid":"","serial_number":"","model_number":"","notify_interval":"","clean_ruleset_threshold":"","clean_ruleset_interval":"","presentation_url":""}}
        case other:
            body = {"data":[id]}
            delete = True

    api_url = event.trigger

    if delete:
        response = requests.delete(api_url, headers=header, json=body)
    else:
        response = requests.put(api_url, headers=header, json=body)

def testSSH(e, header, api_url):
    response = test.changeEventConfig(e, header, api_url)
    ssh = test.connectSSH(e.trigger.split())
    time.sleep(2)
    ssh.close()

def testWeb(e, header, api_url):
    response = test.changeEventConfig(e, header, api_url)
    test.getToken(["hold", e.trigger.split()[0], e.trigger.split()[1]], IP1)
    time.sleep(5)

def testMobData(e, header, api_url):
    trig = e.trigger.split()
    dataOn = {"data":{"modem":"3-1","number":e.nrExpected,"message": trig[0] + " mobileon"}}
    dataOff = {"data":{"modem":"3-1","number":e.nrExpected,"message": trig[0] + " mobileoff"}}
    msg_url = "http://"+IP1+"/api/services/mobile_utilities/sms_messages/send/actions/send"

    if trig[1] == "mobileon":
        requests.post(msg_url, headers=header, json=dataOff)
        time.sleep(5)
    else:
        requests.post(msg_url, headers=header, json=dataOn)
        time.sleep(80)

    response = test.changeEventConfig(e, header, api_url)

    if trig[1] == "mobileon":
        requests.post(msg_url, headers=header, json=dataOn)
        time.sleep(10)
    else:
        requests.post(msg_url, headers=header, json=dataOff)
        time.sleep(5)

    requests.post(msg_url, headers=header, json=dataOn)

def testSimSwitch(e, header, api_url):
    response = test.changeEventConfig(e, header, api_url)

    if e.subtype == "to SIM1":
        sim_url = "http://"+IP1+"/api/network/mobile/simcards/config/cfg02aa0e"
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg02aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        sim_url2 = "http://"+IP1+"/api/network/mobile/sim_switch/config/cfg02aa0e"
        body2 = {"data":{"enabled":"1",".type":"sim","id":"cfg02aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}
    elif e.subtype == "to SIM2":
        sim_url = "http://"+IP1+"/api/network/mobile/simcards/config/cfg01aa0e"
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg01aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        sim_url2 = "http://"+IP1+"/api/network/mobile/sim_switch/config/cfg01aa0e"
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

def testFailover(e, header, api_url, ids):
    get_url = "http://"+IP1+"/api/bulk"
    mainOn = {"data":[{"method": "PUT","endpoint": "/api/network/interfaces/config","data": [{"enabled": "1",".type": "interface","id": ids[0],"metric": "2"}],"awaitNetwork": False}]}
    mainOff = body = {"data":[{"method": "PUT","endpoint": "/api/network/interfaces/config","data": [{"enabled": "0",".type": "interface","id": ids[0],"metric": "2"}],"awaitNetwork": False}]}
    
    if e.trigger == "1": 
        res = requests.post(get_url, headers=header, json=mainOff)
        time.sleep(20)
    else:
        requests.post(get_url, headers=header, json=mainOn)
        time.sleep(20)
    
    response = test.changeEventConfig(e, header, api_url)

    if e.trigger == "1": 
        requests.post(get_url, headers=header, json=mainOn)
        time.sleep(60)
    else:
        requests.post(get_url, headers=header, json=mainOff)
        time.sleep(20)

    requests.post(get_url, headers=header, json=mainOn)

def testPorts(e, header, api_url):
    prep = requests.get("http://"+IP1+"/api/services/port_mirroring/config/general", headers=header)
    if prep.json()['data']['mirror_monitor_port'] == "disabled":
        temp = "1"
    else: 
        temp = "disabled"

    response = test.changeEventConfig(e, header, api_url)
    time.sleep(3)
    requests.put(e.trigger, headers=header, json={"data":{"id":"general",".type":"switch","mirror_monitor_port":temp,"mirror_source_port":"3","enable_mirror_rx":"","enable_mirror_tx":""}})
    time.sleep(10)

def testReboot(e, header, header2, api_url, rut):

    response = test.changeEventConfig(e, header, api_url)
    time.sleep(3)

    match e.subtype:
        case "ping reboot":
            rez = requests.post(e.trigger, headers=header, json={"data":{}})
            tempId = rez.json()['data']['id']
            body = {"data":{".type":"ping_reboot","retry":"1","id":tempId,"ip_type":"ipv4","packet_size":"56","time_out":"1","enable":"1","type":"ping","action":"1","time":"5","host":"192.168.55.55","stop_action":"0","number":"","interface":"1"}}
            rez = requests.put(e.trigger + "/" + tempId, headers=header, json=body)
            time.sleep(420)
            header = {"Authorization": "Bearer " + test.getToken(rut, IP1)}
            requests.delete(e.trigger, headers=header, json={"data":[tempId]})
        case "reboot scheduler":
            dt = datetime.now() + timedelta(seconds=60)
            rez = requests.post(e.trigger, headers=header, json={"data":{}})
            tempId = rez.json()['data']['id']
            body = {"data":{"id":tempId,".type":"reboot_instance","action":"1","period":"week","days":["mon","tue","wed","thu","fri","sat","sun"],"time":[dt.strftime("%H:%M")],"months":"","month_day":"","enable":"1","force_last":""}}
            rez = requests.put(e.trigger + "/" + tempId, headers=header, json=body)
            time.sleep(180)
            header = {"Authorization": "Bearer " + test.getToken(rut, IP1)}
            requests.delete(e.trigger, headers=header, json={"data":[tempId]})
        case "web ui":
            rez = requests.post(e.trigger, headers=header)
            time.sleep(120)
        case "sms reboot":
            body = {"data":{"modem":"3-1","number":e.nrExpected,"message": e.trigger}}
            msg_url = "http://"+IP1+"/api/services/mobile_utilities/sms_messages/send/actions/send"
            rez = requests.post(msg_url, headers=header, json=body)
            print(rez.text)
            time.sleep(120)
        case "from button":
            ssh = test.connectSSH(None)
            #ssh.exec_command(e.trigger)
            test.executeCommand(ssh, e.trigger)
            time.sleep(120)

def testSMS(e, header, api_url):
    response = test.changeEventConfig(e, header, api_url)

    body = {"data":{"modem":"3-1","number":e.nrExpected,"message": e.trigger}}
    msg_url = "http://"+IP1+"/api/services/mobile_utilities/sms_messages/send/actions/send"

    r = requests.post(msg_url, headers=header, json=body)
    time.sleep(8)

def testTopology(e, header, api_url):
    bodyOff = {"data": [{"enabled": "0","id": "wan",".type": "interface","metric": "1"}]}
    bodyOn = {"data": [{"enabled": "1","id": "wan",".type": "interface","metric": "1"}]}
    requests.put(e.trigger, headers=header, json=bodyOff)
    time.sleep(5)
    response = test.changeEventConfig(e, header, api_url)
    requests.put(e.trigger, headers=header, json=bodyOn)
    time.sleep(20)

def testWiFi(e, header, api_url, header2):
    response = test.changeEventConfig(e, header, api_url)

    trig = e.trigger.split() 
    if e.subtype == "client connected":
        body = {"data":{"bssid":trig[0],"ssid":trig[1],"password":trig[2],"network":trig[3],"fwzone":"wan","device":"radio0"}}
        wifi_url = "http://"+IP2+"/api/network/wireless/devices/actions/join_wifi_network"
        z = requests.post(wifi_url, headers=header2, json=body)
        time.sleep(5)
    elif e.subtype == "client disconnected":
        body = {"data":[trig[0]]}
        wifi_url = "http://"+IP2+"/api/network/interfaces/config"
        z = requests.delete(wifi_url, headers=header2, json=body)

    time.sleep(10)

def testDHCP(e, header, api_url, header2):
    trig = e.trigger.split() 
    dhcp_url = "http://"+IP1+"/api/network/dhcp/servers/config/lan"
    bodyChange = {"data": {"end_ip": "192.168.1."+trig[3],"start_ip": "192.168.1."+trig[2],"leasetime": "10h"}}
    bodyOG = {"data": {"end_ip": "192.168.1."+trig[1],"start_ip": "192.168.1."+trig[0]},"leasetime": "10h"}

    bodyUpdate = {"data": {".type": "interface","fwzone": "lan","id": "lan","ip6assign": "60","ifname": ["eth0"],"proto": "static"}}
    update_url = "http://"+IP1+"/api/network/interfaces/config/lan"

    response = test.changeEventConfig(e, header, api_url)
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
        wifi_url = "http://"+IP2+"/api/network/wireless/devices/actions/join_wifi_network"
        requests.post(wifi_url, headers=header2, json=body)
        time.sleep(60)
        body = {"data":[trig[3]]}
        wifi_url = "http://"+IP2+"/api/network/interfaces/config"
        aaa = requests.delete(wifi_url, headers=header2, json=body)