#!/usr/bin/env python

import subprocess 
import optparse
import re
import os 
import random
import datetime
import time
import json

history_file  = os.path.expanduser("~/.Mac_Address_History")
file_path = os.path.expanduser("~/.mac_changer_backup")

def get_arguments():
    if os.geteuid() != 0:
        print("-" * 60)
        print()
        print("[-] ROOT REQUIRED")
        print()
        print("-" * 60)
        exit(1)

    parse = optparse.OptionParser()

    parse.add_option("-i", "--Interface", dest="INTERFACE", help="Enter the Interface name to change it")
    parse.add_option("-m", "--mac", dest="MAC_ADDRESS", help="Enter your custom mac address")
    parse.add_option("-r", "--random", action="store_true", dest="RANDOM", default=False, help="Random Mac address will be generated")
    parse.add_option("-e", "--restore", default=False, action="store_true", dest="RESTORE", help="Change to the previous mac address.")
    parse.add_option("-H", "--history", dest="HISTORY", default=False, action="store_true", help="Show's the old mac, new mac and the interface name with timestamps")
    parse.add_option("-s","--Stealth", default= False, type=int,dest= "STEALTH" ,help="change the MAC address for every N interval of time")

    (options, arguments) = parse.parse_args()

    if options.HISTORY:
        show_history()
        exit(0)


# The parse.error ends the program by themself so exit(0) not required
    if not options.INTERFACE:
        parse.error("[-] Kindly enter a interface name or use --help")
    elif options.RANDOM:
        options.MAC_ADDRESS = New_mac_generator()
        print()
        print(f"[+] Your new MAC ADDRESS {options.MAC_ADDRESS}")
        print()
    elif options.RESTORE:
        options.MAC_ADDRESS = Restore_MAC_address(options.INTERFACE) 
        print(f"[+] Old Mac Address restored {options.MAC_ADDRESS}")
    elif options.STEALTH:
        return options.INTERFACE, None , options.STEALTH # if stealth mode then we dont need the mac address from the user
    elif not options.MAC_ADDRESS:
        parse.error("Enter a MAC address or use --help or -r")
    
        

    m = options.MAC_ADDRESS

    if not re.match(r"^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$", m): #validating if its a valid mac address 
        print("-" * 60)
        print()
        print("[-] Invalid MAC address")
        print("-" * 60)
        print()
        exit(1)
    
    inf = options.INTERFACE

    if inf.lower() == "lo": # if the interface is Local Host then reject it.
            print()
            print("-" *50)
            print("[-] Sorry but this interface cant be accepted")
            print()
            print("-" *50)
            exit(1)
    try:
        subprocess.check_call(                   # validating if its a valid interface 
            ["ifconfig", options.INTERFACE],
            stdout = subprocess.DEVNULL,
            stderr = subprocess.DEVNULL
            )
    except subprocess.CalledProcessError:
        print("-" * 60)
        print()
        print(f"[-] Interface {options.INTERFACE} not found")
        print("Try doing ifconfig -a to see the other options")
        print("-" * 60)
        print()
        exit(1)    
    
    return options.INTERFACE,options.MAC_ADDRESS, None
    
    

def New_mac_generator():
    new_mac = [0x02]+[random.randint(0x00, 0xff) for _ in range(5)]
    return  ":".join(f"{byte:02x}" for byte in new_mac)



# takes the mac address and saves it in the file path
def save_mac_history(interface):
    output = subprocess.check_output(["ifconfig",interface]).decode("utf-8")
    result = re.search(r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}", output)
    mac = result.group(0)
    
    data = {}
    if os.path.exists(file_path): 
      # if the file does not exist then it will go to the next if block and there the file will be created.
      with open(file_path,"r") as f:  
        try:   # this is for a backup as json cant append new lines and if we do then the old data is lost 
             data = json.load(f)
        except json.JSONDecodeError:
            pass

# done only when a new interface is typed
    if interface not in data:
        data[interface] = mac
        with open(file_path, "w") as f:
            json.dump(data,f)
        print(f"[+] Original Mac address saved")
    


# checks if the file path exists if yes it will return the mac address
def Restore_MAC_address(interface):
    # done so that if the user types -e in the very start then it will stop the user
    if not os.path.exists(file_path):
        print(f"[-] Restore cant be performed, did u run the program once?")
        exit(1)

    with open(file_path,"r") as f:
        data = json.load(f)
    
    if interface in data:
        print(f"[+] Original mac address for the interface {interface} restored")
        return data[interface]
    else:
        print(f"[-] No Backup found for this interfcae")
        exit(1)

def save_history(interface,old_mac,new_mac):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    if not os.path.exists(history_file):
        with open(history_file,"w") as f:
            f.write("TIMESTAMP            | INTERFACE | OLD MAC           | NEW MAC\n")
            f.write("-" * 72 + "\n")


    with open(history_file, "a") as f:
        f.write(f"{time_stamp} | {interface}      | {old_mac} | {new_mac}\n")
    print(f"[+] History saved")


def show_history():
    if not os.path.exists(history_file):
        print(f"""[-] history file is empty.
        change the mac address to see the history file """)
        return
    
    print("*" *72)
    print()
    print(" \t\t\t  MAC ADDRESS HISTORY")
    print()
    print("*" *72)
    with open(history_file,"r") as f:
        print(f.read())
    

def change_mac_address(interface, mac):
    print("-" * 60)

    interface_name = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
     
     # to check if the interface provided has a MAC address or not
    old_mac = re.search(r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}", interface_name)
    if not old_mac:
        print(f"""[-] The interface {interface} does not have an MAC Address. 
        Try with a different interface""")
        print("-" * 60)
        exit(1) 
     
    print(f"[+] Your current mac address: {old_mac.group(0)}")
    print(f"[+] changing MAC address for {interface} to {mac}")

    try:
     subprocess.check_call(["ifconfig", interface, "down"])
     subprocess.check_call(["ifconfig", interface, "hw", "ether", mac])
     subprocess.check_call(["ifconfig", interface, "up"])
     
     result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")

     new_mac = re.search(r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}", result)

     
     if new_mac.group(0).lower() == old_mac.group(0).lower():
         print("[-] MAC address did not change")
         return
     else:
        print("[+] DONE!")
        print("[+] check the new MAC address")
        print()
        subprocess.call(["ifconfig", interface])
        print()
        print("[+] Thank you")
        save_history(interface, old_mac.group(0), new_mac.group(0)) # saving in the history file
        print("-" * 60)

    except subprocess.CalledProcessError as e:
        print("Enter valid details")
        return
    

def Stealth_mode(interface,interval):
    print("*" * 60)
    print()
    print("\t\t STEALTH MODE")
    print()
    print("*" * 60)
    

    output = subprocess.check_output(["ifconfig",interface]).decode("utf-8")
    mac = re.search(r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}", output)

    print(f"[+] Your original ip address {mac.group(0)}")
 
    try:

      while True:
        print()
        new_mac = New_mac_generator()
        print(f"[+] changing the mac address.....")
        change_mac_address(interface,new_mac)
        print(f"[+] Your new Mac address is {new_mac}")
        print(f"[+] The next change is in {interval} minutes.... ")
        time.sleep(interval * 60) # because sleep takes time in seconds and we r converting it into minutes.
        print()
        print()

    except KeyboardInterrupt as e:
          print("[+] Thank You")
    

interface,mac,stealth_interval = get_arguments()

if stealth_interval:
    save_mac_history(interface)
    Stealth_mode(interface,stealth_interval)   
else:     
    save_mac_history(interface)
    change_mac_address(interface, mac)

