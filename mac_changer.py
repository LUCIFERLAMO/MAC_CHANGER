#!/usr/bin/env python

import subprocess 
import optparse
import re
import os 
import random

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
    parse.add_option("-t", "--restore", default=False, action="store_true", dest="RESTORE", help="Change to the previous mac address.")

    (options, arguments) = parse.parse_args()

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
    
    return options.INTERFACE,options.MAC_ADDRESS
    
    
def New_mac_generator():
    new_mac = [0x02]+[random.randint(0x00, 0xff) for _ in range(5)]
    return  ":".join(f"{byte:02x}" for byte in new_mac)


file_path = os.path.expanduser("~/.mac_changer_backup")

# takes the mac address and saves it in the file path
def save_mac(interface):
    output = subprocess.check_output(["ifconfig",interface]).decode("utf-8")
    mac = re.search(r"([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}", output)

    if os.path.exists(file_path): 
      with open(file_path,"r") as f:   
        saved_mac = f.read().strip()
      if saved_mac.lower() == mac.group(0).lower(): #checking if the mac address saved in the file is same as the incomming mac address 
        print(f"[-] MAC already saved, skipping backup")
        return
    
    with open(file_path,"w") as f:
          f.write(mac.group(0))
    print(f"[+] MAC address saved")


# checks if the file path exists if yes it will return the mac address
def Restore_MAC_address(interface):
    if not os.path.exists(file_path):
        print(f"[-] Restore cant be performed, did u run the program once?")
        exit(1)
    with open(file_path,"r") as f:
        return f.read().strip()


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
        print("-" * 60)

    except subprocess.CalledProcessError as e:
        print("Enter valid details")
        return


interface,mac = get_arguments()
save_mac(interface)
change_mac_address(interface, mac)

