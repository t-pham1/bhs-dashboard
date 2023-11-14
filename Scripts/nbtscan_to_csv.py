from termcolor import colored
import re
import ipaddress
import pandas as pd

ONLINE_STATUS = 4
OFFLINE_STATUS = 5
NODE_ID = 1
WORKSTATION_ID = 2

# collected from nbtscan
ip_address, mac_address, name, status_id = [], [], [], []

with open("online.txt", 'r') as file:
    for line in file:
        # more parsing
        line = line.replace('\n', '')
        line = line.replace(' ', '')
        
        ip_name_mac = re.split(',', line)
        ip_address.append(ip_name_mac[0])
        # cases for when name is null
        if len(ip_name_mac) < 3:
            name.append("N/A")
            mac_address.append(ip_name_mac[1])
        else:
            name.append(ip_name_mac[1])
            mac_address.append(ip_name_mac[2])
        
        status_id.append(ONLINE_STATUS)

num_nodes, num_workstations = 180, 255
total = num_nodes + num_workstations

num_online = len(ip_address)
num_offline = total - num_online

# get offline ip addresses
curr = 1
for i in range(255): # workstations
    temp = "10.1.10." + str(curr)
    
    curr += 1
    
    if ip_address.count(temp) == 0:
        ip_address.append(temp)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)

curr = 1
for i in range(40): # nodes
    temp0 = "10.1.50." + str(curr)
    temp1 = "10.1.51." + str(curr)
    temp2 = "10.1.52." + str(curr)
    temp3 = "10.1.53." + str(curr)
    temp4 = "10.1.54." + str(curr)
    
    curr += 1
    
    if ip_address.count(temp0) == 0:
        ip_address.append(temp0)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)
    if ip_address.count(temp1) == 0:
        ip_address.append(temp1)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)
    if ip_address.count(temp2) == 0:
        ip_address.append(temp2)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)
    if ip_address.count(temp3) == 0:
        ip_address.append(temp3)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)
    if ip_address.count(temp4) == 0 and curr <= 21: #5th rack only has 20 nodes
        ip_address.append(temp4)
        mac_address.append("NULL")
        name.append("NULL")
        status_id.append(OFFLINE_STATUS)

# sort by ip address
temp = [ipaddress.IPv4Address(ip) for ip in ip_address]
sorted_ip, sorted_mac, sorted_name, sorted_status_id = sorted(temp), [], [], []

# not included in nbtscan (required snipe-it fields/mysql columns)
id, asset_tag, category, manufacturer, model_name, model_id = [], [], [], [], [], []

curr = 1
for i in range(len(ip_address)):
    sorted_ip[i] = str(sorted_ip[i])
    
    id.append(i+1)
    asset_tag.append(i+1)
    
    if sorted_ip[i][5:7] == "10":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.10." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
        
        category.append("Workstations")
        manufacturer.append("N/A")
        model_name.append("N/A")
        model_id.append(WORKSTATION_ID)
    
    if sorted_ip[i][5:7] == "50":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.50." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
    
    if sorted_ip[i][5:7] == "51":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.51." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
    
    if sorted_ip[i][5:7] == "52":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.52." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
    
    if sorted_ip[i][5:7] == "53":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.53." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
    
    if sorted_ip[i][5:7] == "54":
        curr = int(sorted_ip[i][8:])
        index = ip_address.index("10.1.54." + str(curr))
        
        sorted_mac.append(mac_address[index])
        sorted_name.append(name[index])
        sorted_status_id.append(status_id[index])
    
    if sorted_ip[i][5:7] == "50" or sorted_ip[i][5:7] == "51" or sorted_ip[i][5:7] == "52" or sorted_ip[i][5:7] == "53" or sorted_ip[i][5:7] == "54":
        category.append("Nodes")
        manufacturer.append("Mellanox Technologies")
        model_name.append("N/A")
        model_id.append(NODE_ID)

ip_address, mac_address, name, status_id = sorted_ip, sorted_mac, sorted_name, sorted_status_id

dict = {"ID": id, "asset_tag": asset_tag, "Category": category, "Name": name, "IP Address": ip_address, "MAC Address": mac_address, "Status": status_id, "Manufacturer": manufacturer, "Model Name": model_name, "model_id": model_id}
df = pd.DataFrame(dict)
df.set_index("ID", inplace=True)
df.to_csv("spreadsheet.csv")

print("SPREADSHEET UPDATED (" + str(total) + " IP ADDRESSES SCANNED): " + colored(str(num_online) + " ONLINE", "white", "on_green") + ' ' + colored(str(num_offline) + " OFFLINE", "white", "on_red") + '\n')