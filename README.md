# Events Reporting Testing
#### Intro
This python program is made to test the Events Reporting Service functionality in any router that supports SMS.
#### Prerequisites
Before you begin, these are the libraries you will need to install:
```
pip install paramiko
pip install argparse
```
Then you must connect your desired device to your computer using an ethernet cable. Navigate to it's WebUI and add a new  events reporting rule in Services>Events Reporting, leave it empty. Next you have to insert your SIM cards in both your main router plus your secondary router that will be receiving the resulting messages. Connect the main router to the second one via ethernet cable and make sure they are in the same lan subnet. You must also have a another direct source of internet to be able to test the failover event rule.
#### Program
You can run the program using:
```
python3 main.py [--name] "router name" [--file] "config file location" [--rut1] "Main router parameters" [--rut2] "Second router parameters"
```
The router name and file are mandatory arguments and must be pasted correctly. Both router variables are optional if you decide to customize your connection and want to set your own variables for the ip, username and password. The default for rut1 - 192.168.1.1 admin Admin123, rut2 - 192.168.1.2 admin Admin123. Here are a few examples of how to use the program:
```
python3 main.py --name RUTX11 --file Config/config.json
python3 main.py --name RUT955 --file /home/stud/testfile.json --rut1 192.168.2.1 user passwd --rut2 192.168.2.5 admin 12345
```
While running the program you will be able to see live results like the events type and subtype, total number of commands to be tested, how many commands passed and failed the test.
#### Files
The command file must be a .json and it's format you can see in the example below. In it you must have the second routers phone number, a list of devices with the name and their own phone number. The device has a list of event types and inside them are their subtypes. The subtype name must be the one found in the API, not the one found on the WebUI. Different subtypes have different triggers. For instance, the config type and it's subtypes all have triggers that are just the endpoint. However, the DHCP type's lan subtype requires four numbers, first two are your desired DHCP from and to IPs, the second two are ones that are going to trigger the event rule. You can observe the different variations in the example:
```
{
    "testNumber":"864781254",
    "devices": [
        {
            "router": "RUTX11",
            "number": "865843255",
            "types": [
                {
                    "type": "Config",
                    "subtypes": [
                        {
                            "subtype": "wireless",
                            "trigger": "http://192.168.1.1/api/network/wireless/devices/config/radio0",
                            "expected":"Wireless"
                        },
                        {
                            "subtype": "profiles",
                            "trigger": "http://192.168.1.1/api/system/profiles/config",
                            "expected":"Profiles"
                        },
                        {
                            "subtype": "mosquitto",
                            "trigger": "http://192.168.1.1/api/services/mqtt_broker/config/general",
                            "expected":"MQTT Broker"
                        }
                    ]
                },
                {
                    "type": "DHCP",
                    "subtypes": [
                        {
                            "subtype": "lan",
                            "trigger": "100 150 50 80",
                            "expected":"LAN"
                        },
                        {
                            "subtype": "wifi",
                            "trigger": "00:1E:42:24:D7:18 RUT_D718_2G Ua98KhZz test",
                            "expected":"WiFi"
                        }
                    ]
                },
                {
                    "type": "SIM switch",
                    "subtypes": [
                        {
                            "subtype": "to SIM2",
                            "trigger": "",
                            "expected":"Switched to SIM2"
                        }
                    ]
                },
                {
                    "type": "WiFi",
                    "subtypes": [
                        {
                            "subtype": "client connected",
                            "trigger": "00:1E:42:24:D7:18 RUT_D718_2G Ua98KhZz test",
                            "expected":"Client Connected"
                        }
                    ]
                },
                {
                    "type": "SMS",
                    "subtypes": [
                        {
                            "subtype": "received from",
                            "trigger": "Hello",
                            "expected":"SMS Received"
                        }
                    ]
                },
                {
                    "type": "Reboot",
                    "subtypes": [
                        {
                            "subtype": "from button",
                            "trigger": "reboot -b",
                            "expected": "Rebooted From Button"
                        },
                        {
                            "subtype": "reboot scheduler",
                            "trigger": "http://192.168.1.1/api/services/auto_reboot/periodic/config",
                            "expected": "Rebooted From Scheduler"
                        }
                    ]
                },
                {
                    "type": "Switch Events",
                    "subtypes": [
                        {
                            "subtype": "Port link state",
                            "trigger": "http://192.168.1.1/api/services/port_mirroring/config/general",
                            "expected": "Port Link State Change"
                        }
                    ]
                }
            ]
        },
        {
            "router": "RUT956",
            "number": "867822518",
            "types": [
                {
                    "type": "Failover",
                    "subtypes": [
                        {
                            "subtype": "Switched to main",
                            "trigger": "1",
                            "expected":"Switched To Main"
                        }
                    ]
                },
                {
                    "type": "Web UI",
                    "subtypes": [
                        {
                            "subtype": "was successful",
                            "trigger": "admin Admin123",
                            "expected":"WebUI Login Successful"
                        }
                    ]
                },
                {
                    "type": "SSH",
                    "subtypes": [
                        {
                            "subtype": "succeeded",
                            "trigger": "192.168.1.1 root Admin123",
                            "expected":"SSH Login Successful"
                        }
                    ]
                },
                {
                    "type": "Mobile Data",
                    "subtypes": [
                        {
                            "subtype": "data connected",
                            "trigger": "Admin123 mobileon",
                            "expected":"Mobile Data Connected"
                        }
                    ]
                },
                {
                    "type": "Switch Topology",
                    "subtypes": [
                        {
                            "subtype": "Changes in topology",
                            "trigger": "http://192.168.1.1/api/network/interfaces/config",
                            "expected":"Changes In Topology"
                        }
                    ]
                }
            ]
        }
    ]
}
```
Results are stored in the Results folder in .csv format. A new file is created for every time you launch a test.