#!/usr/bin/env python

import subprocess 
import optparse
import re
import os 

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

    (options, arguments) = parse.parse_args()

# The parse.error ends the program by themself so exit(0) not required
    if not options.INTERFACE:
        parse.error("[-] Kindly enter a interface name or use --help")
    elif not options.MAC_ADDRESS:
        parse.error("[-] kindly enter the mac address or use --help")
    

    m = options.MAC_ADDRESS

    if not re.match(r"^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$", m):
        print("-" * 60)
        print()
        print("[-] Invalid MAC address")
        print("-" * 60)
        print()
        exit(1)
    
    try: 
        subprocess.check_call(
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
change_mac_address(interface, mac)
    
