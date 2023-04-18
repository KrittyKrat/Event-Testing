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
        case "xl2tpd":
            body = {"data":{"id":str(random.randrange(9999)),".type":"service"}}
            post = True
        case "widget":
            body = [{"jsonrpc":"2.0","id":24,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","set",{"config":"widget","section":"cfg028e09","values":{"enabled":"0"}}]}]
            post = True
        case "sqm":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "sms_utils":
            body = {"data":{"smstext":"12345","action":"gps"}}
            post = True
        case "rpcd":
            body = {"data":{"username":str(random.randrange(9999)),"password":"Asdasd123","group":"user"}}
            post = True
        case "pptpd":
            body = {"data":{"id":str(random.randrange(9999)),".type":"service"}}
            post = True
        case "operctl":
            body = {"data":{"name":str(random.randrange(9999))}}
            post = True
        case "mwan3":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
        case "mwan3":
            body = {"data":{"id":str(random.randrange(9999))}}
            post = True
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
        case "ip_blockd":
            body = {"data":{"enabled":"0",".type":"globals","max_attempt_count":"10","id":"general","reboot_clear":"0"}}
        case "frr":
            body = [{"jsonrpc":"2.0","id":25,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","set",{"config":"frr","section":"bgp","values":{"enabled":True}}]},{"jsonrpc":"2.0","id":26,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","delete",{"config":"frr","section":"main_instance","options":["redistribute"]}]}]
        case "email_to_sms":
            body = {"data":{"enabled":"1",".type":"pop3","limit":"5","id":"general","host":"test.com","port":"80","username":"Asd","password":"Asdasd123","ssl":"0","time":"min","min":"1"}}
        case "avl":
            body = {"data":{"enabled":"1","static_navigation":"0","id":"general","con_cont":"0","port":"8501","hostname":"192.168.0.1","proto":"tcp","send_retry":"0",".type":"section"}}
        case "dhcp":
            body = {"data":{".type":"dhcp","id":"lan","ignore":"enable","end_ip":"192.168.1.150","leasetime":"12h","force":"0","start_ip":"192.168.1.100","dynamicdhcp":"0","netmask":"","dhcp_option":[],"force_options":"0","ra":"","dhcpv6":"","ndp":"","dns":[],"domain":[]}}
        case "etherwake":
            body = {"data":{"id":"general","broadcast":"1",".type":"etherwake"}}
        case "post_get":
            body = {"data":{"password":"Asdasd123",".type":"post_get","allow":["io_state","io_type","io_value"],"id":"general","enabled":"1","username":"asd","password_confirm":"Asdasd123"}}
        case "stunnel":
            body = {"data":{"id":"general",".type":"globals","enabled":"1","debug":"5","use_alt":"0"}}
        case "snmptrap":
            body = {"data":{"enabled":"1",".type":"server","community":"public","id":"general","host":"","port":"162"}}
        case "snmpd":
            body = {"data":{"enabled":"1","v2cmode":"1","v1mode":"1","ipfamily":"ipv4","port":"161","id":"general",".type":"agent","remoteAccess":"0","v3mode":"0"}}
        case "sms_gateway":
            body = {"data":{"enabled":"1",".type":"reply","delete_sms":"0","id":"general","mode":"everyone","every_sms":"0","tel":"","msg":"Hello"}}
        case "simcard":
            body = {"data":{"volte":"auto","deny_roaming":"0","service":"auto","pincode":"1234","signal_reset_enabled":"0","band":"auto",".type":"sim","id":"cfg01aa0e","primary":"1","sms_limit":"day","enable_sms_limit":"1","period":"0","sms_limit_num":"5000","operlist":"0"}}
        case "sim_switch":
            body = {"data":{"retry_count":"3","no_network":"0","on_signal":"0","interval":"10","enabled":"1",".type":"sim","id":"cfg01aa0e","denied":"0","weak_signal":"","data_limit":"0","roaming":"0","data_fail":"","fail_flag":"0","sms_limit":"0"}}
        case "samba":
            body = {"data":{"workgroup":"WORKGROUP",".type":"samba","description":"Router share","id":"general","name":"Router_share","homes":"1","enabled":"1"}}
        case "rms_mqtt":
            body = {"data":{".type":"rms_connect_mqtt","enable":"1","id":"general","remote":"rms.teltonika-networks.com","port":"10"}}
        case "quota_limit":
            body = {"data":{"force_apn":"3200","fwzone":"wan","sim":"1","metric":"4","delegate":"1","force_link":"0","proto":"wwan","method":"nat",".type":"interface","id":"mob1s1a1","pdptype":"ip","auto_apn":"0","dns":[],"mtu":"","ip4table":"","mob_limit_enabled":"1","period":"day","reset_hour":"0","enable_warning":"0","data_limit":"1000"}}
        case "privoxy":
            body = {"data":{"enabled":"1","_mode":"blacklist","id":"general",".type":"privoxy","url":[]}}
        case "p910nd":
            body = {"data":{"enabled":"1","port":"9100","device":"/dev/usb/lp0","id":"general",".type":"p910nd","bidirectional":"1"}}
        case "overview":
            body = {"data":[{"id":"cfg010a5c","position":"1","enabled":"0"}]}
        case "ntpserver":
            body = {"data":{"enabled":"1",".type":"ntpserver","id":"general"}}
        case "ntpclient":
            body = {"data":{"enabled":"1",".type":"ntpclient","freq":"0","interval":"86400","id":"general","save":"0","force":"0","count":"","sync_enabled":"0","tmz_sync_enabled":"1"}}
        case "modbusgateway":
            body = {"data":{"enabled":"1",".type":"gateway","id":"general","response":"response","host":"127.0.0.1","port":"1883","request":"request","keepalive":"5","qos":"2","tls":"0","user":"","pass":"","client_id":""}}
        case "modbus":
            body = {"data":{".type":"modbus","id":"general","keepconn":"1","allow_ra":"0","enabled":"1","port":"502","device_id":"1","md_data_type":"0","timeout":"0","clientregs":"0"}}
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

    try:
        return response.json()['data']['id']
    except:
        return ""

def deleteTemp(header, event, id):

    delete = False
    match event.subtype:
        case "ip_blockd":
            body = {"data":{"enabled":"1",".type":"globals","max_attempt_count":"10","id":"general","reboot_clear":"0"}}
        case "frr":
            body = {"jsonrpc":"2.0","id":27,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","apply",{"timeout":10}]}
        case "email_to_sms":
            body = {"data":{"enabled":"0",".type":"pop3","limit":"5","id":"general","host":"test.com","port":"80","username":"Asd","password":"Asdasd123","ssl":"0","time":"min","min":"1"}}
        case "avl":
            body = {"data":{"enabled":"0","static_navigation":"0","id":"general","con_cont":"0","port":"8501","hostname":"192.168.0.1","proto":"tcp","send_retry":"0",".type":"section"}}
        case "dhcp":
            body = {"data":{".type":"dhcp","id":"lan","ignore":"enable","end_ip":"192.168.1.150","leasetime":"12h","force":"0","start_ip":"192.168.1.100","dynamicdhcp":"1","netmask":"","dhcp_option":[],"force_options":"0","ra":"","dhcpv6":"","ndp":"","dns":[],"domain":[]}}
        case "etherwake":
            body = {"data":{"id":"general","broadcast":"0",".type":"etherwake"}}
        case "widget":
            body = {"jsonrpc":"2.0","id":25,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","apply",{"timeout":10}]}
        case "post_get":
            body = {"data":{"enabled":"0",".type":"post_get","allow":["io_state","io_type","io_value"],"id":"general","username":"asd","password_confirm":""}}
        case "stunnel":
            body = {"data":{"id":"general",".type":"globals","enabled":"0","debug":"5","use_alt":"0"}}
        case "snmptrap":
            body = {"data":{"enabled":"0",".type":"server","community":"public","id":"general","host":"","port":"162"}}
        case "snmpd":
            body = {"data":{"enabled":"0","v2cmode":"1","v1mode":"1","ipfamily":"ipv4","port":"161","id":"general",".type":"agent","remoteAccess":"0","v3mode":"0"}}
        case "sms_gateway":
            body = {"data":{"enabled":"0",".type":"reply","delete_sms":"0","id":"general","mode":"everyone","every_sms":"0","tel":"","msg":"Hello"}}
        case "simcard":
            body = {"data":{"volte":"auto","deny_roaming":"0","service":"auto","pincode":"1234","signal_reset_enabled":"0","band":"auto",".type":"sim","id":"cfg01aa0e","primary":"1","sms_limit":"day","enable_sms_limit":"0","period":"0","sms_limit_num":"5000","operlist":"0"}}
        case "sim_switch":
            body = {"data":{"retry_count":"3","no_network":"0","on_signal":"0","interval":"10","enabled":"0",".type":"sim","id":"cfg01aa0e","denied":"0","weak_signal":"","data_limit":"0","roaming":"0","data_fail":"","fail_flag":"0","sms_limit":"0"}}
        case "samba":
            body = {"data":{"workgroup":"WORKGROUP",".type":"samba","description":"Router share","id":"general","name":"Router_share","homes":"1","enabled":"0"}}
        case "rms_mqtt":
            body = {"data":{".type":"rms_connect_mqtt","enable":"1","id":"general","remote":"rms.teltonika-networks.com","port":"15009"}}
        case "quota_limit":
            body = {"data":{"force_apn":"3200","fwzone":"wan","sim":"1","data_limit":"","enable_warning":"","metric":"4","delegate":"1","force_link":"0","proto":"wwan","method":"nat",".type":"interface","id":"mob1s1a1","reset_hour":"","mob_limit_enabled":"0","period":"","pdptype":"ip","auto_apn":"0","dns":[],"mtu":"","ip4table":""}}
        case "privoxy":
            body = {"data":{"enabled":"0","_mode":"blacklist","id":"general",".type":"privoxy","url":[]}}
        case "p910nd":
            body = {"data":{"enabled":"0","port":"9100","device":"/dev/usb/lp0","id":"general",".type":"p910nd","bidirectional":"1"}}
        case "overview":
            body = {"data":[{"id":"cfg010a5c","position":"1","enabled":"1"}]}
        case "ntpserver":
            body = {"data":{"enabled":"0",".type":"ntpserver","id":"general"}}
        case "ntpclient":
            body = {"data":{"enabled":"1",".type":"ntpclient","freq":"0","interval":"86400","id":"general","save":"0","force":"0","count":"","sync_enabled":"0","tmz_sync_enabled":"0"}}
        case "modbusgateway":
            body = {"data":{"enabled":"0",".type":"gateway","id":"general","response":"response","host":"127.0.0.1","port":"1883","request":"request","keepalive":"5","qos":"2","tls":"0","user":"","pass":"","client_id":""}}
        case "modbus":
            body = {"data":{".type":"modbus","id":"general","keepconn":"1","allow_ra":"0","enabled":"0","port":"502","device_id":"1","md_data_type":"0","timeout":"0","clientregs":"0"}}
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

    match event.subtype:
        case "multi_wifi":
            body2 = {"data":{"enabled":"1",".type":"wifi-iface","network":"Test","encryption":"none","id":"1","ssid":"multi_ap","disassoc_low_ack":"1","short_preamble":"1","mode":"sta","bssid":"","dtim_period":"","wpa_group_rekey":"","skip_inactivity_poll":"0","max_inactivity":"","max_listen_interval":"","r0kh":"","r1kh":""}}
            api_url = "http://192.168.1.1/api/network/wireless/devices/config/radio0/interfaces"
            api_url2 = api_url+"/"+str(id)
            requests.put(api_url2, headers=header, json=body2)
        case "widget":
            body2 = [{"jsonrpc":"2.0","id":24,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","set",{"config":"widget","section":"cfg028e09","values":{"enabled":"1"}}]}]
            api_url = event.trigger
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body)
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body2)
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body)
            return
        case "frr":
            body2 = [{"jsonrpc":"2.0","id":25,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","set",{"config":"frr","section":"bgp","values":{"enabled":False}}]},{"jsonrpc":"2.0","id":26,"method":"call","params":["fbd73545588e8f2d0874ac6d1fa95dde","uci","delete",{"config":"frr","section":"main_instance","options":["redistribute"]}]}]
            api_url = event.trigger
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body)
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body2)
            time.sleep(1)
            response = requests.post(api_url, headers=header, json=body)
            return
        case other:
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
        time.sleep(10)
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
    time.sleep(30)

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
    time.sleep(100)

    if e.subtype == "to SIM1":
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg02aa0e","primary":"0","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        body2 = {"data":{"enabled":"0",".type":"sim","id":"cfg02aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}
    elif e.subtype == "to SIM2":
        body = {"data":{"band":"auto","volte":"auto","deny_roaming":"0","id":"cfg01aa0e","primary":"1","pincode":"1234","signal_reset_enabled":"0","enable_sms_limit":"0",".type":"sim","service":"auto","operlist":"0"}}
        body2 = {"data":{"enabled":"0",".type":"sim","id":"cfg01aa0e","on_signal":"1","data_limit":"0","sms_limit":"0","roaming":"0","no_network":"1","denied":"1","fail_flag":"1","interval":"10","retry_count":"3","weak_signal":"-1","data_fail":"1"}}

    requests.put(sim_url2, headers=header, json=body2)
    time.sleep(10)
    requests.put(sim_url, headers=header, json=body)
    time.sleep(120)

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
            time.sleep(400)
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
    time.sleep(60)

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