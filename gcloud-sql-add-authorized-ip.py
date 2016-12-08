# *********************
# Script to authorize add an IP addres to sql authorized network
# Usage: 'gcloud-sql-add-authorized-ip [command: add|remove] [IP-CIDR-notation]'
# about CIDR notation https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation
# Sample: 'gcloud-sql-add-authorized-ip add 10.10.10.10/24'
# Author: Doers DF (hola@doersdf.com)
# ********************

import json
import subprocess
import sys
import re
pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$")


if len(sys.argv)==3:
    newIP = sys.argv[2]
    command = sys.argv[1]
    if pattern.match(newIP)==None:
        print("[203] Error: Invalid IP.\n   Use IP CIDR notation Sample 'gcloud-sql-add-authorized-ip add 192.168.0.1/24'' ")
    elif command!="add" and command!="remove":
        print("[202] Error: Invalid command.\n   Use Add or Remove 'gcloud-sql-add-authorized-ip add 192.168.0.1/24'' ")
    else: 
        #call google cloud sql api to get configuration in json format
        
        p = subprocess.Popen("gcloud sql instances describe steps-sql --format json", shell=True, stdout=subprocess.PIPE)
        p.wait()

        out, err = p.communicate()
        data = json.loads(out)
        

        ips = ""
        IPfound =False
        print("Current Authorized Networks",  data["settings"]["ipConfiguration"]["authorizedNetworks"])
        for ip in data["settings"]["ipConfiguration"]["authorizedNetworks"]:
            if newIP==ip:
                IPfound=True
            else:
                ips = ips + "," + ip    

        if (command =="add" and IPfound==False) or (command=="remove" and IPfound==True):
            if command=="add":
                ips = newIP + ips
            else:
                ips = ips[1:]
            p = subprocess.Popen("gcloud sql instances patch steps-sql --authorized-networks=" + ips, shell=True, stdout=subprocess.PIPE)
            p.wait()
            print("[100] OK. Current authorizedNetworks = " + ips)
        else:
            if command =="add":
                print("[200] Warning: Especified IP already authorized. Nothing done.")
            else:
                print("[200] Warning: Especified IP not found. Nothing done.")
              
else:
    print("[201] Error: 2 argument required.\n   Usage 'gcloud-sql-add-authorized-ip.py add 192.168.0.1/24 ")

