#!/usr/bin/env python

import subprocess 
import optparse

def change_mac_address(interface, mac):
    print("-" * 60)
    print()
    print(f"[+] changing MAC address for {interface} to {mac}")
    
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])
    
    print("[+] DONE!")
    print("[+] check the new MAC address")
    print()
    subprocess.call(["ifconfig", interface])
    print()
    print("[+] Thank you")
    print("-" * 60)

parse = optparse.OptionParser()

parse.add_option("-i", "--Interface", dest="INTERFACE", help="Enter the Interface name to change it")
parse.add_option("-m", "--mac", dest="MAC_ADDRESS", help="Enter your custom mac address")

(options, arguments) = parse.parse_args()

change_mac_address(options.INTERFACE, options.MAC_ADDRESS)
    
