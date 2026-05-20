#!/usr/bin/env python

import subprocess 

print("-" * 60)


interface = input("Enter the interface (eth0): ")
if interface != "eth0":
    print("Invalid choose from the given option")
    exit(0)
      
new_mac = input("Enter a mac address (12 numbers/characters): ")
print()
print(f"[+] changing MAC address for {interface} to {new_mac}")

subprocess.call(["ifconfig", interface, "down"])
subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["ifconfig", interface, "up"])

print("[+] DONE!")
print("[+] check the new MAC address")
print()
subprocess.call(["ifconfig"])
print()
print("[+] Thank you")

print("-" * 60)