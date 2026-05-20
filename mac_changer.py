#!/usr/bin/env python

import subprocess 

print("-" * 60)


interface = input("Enter the interface (eth0): ")
new_mac = input("Enter a mac address (12 numbers/characters): ")
print()
print(f"[+] changing MAC address for {interface} to {new_mac}")

subprocess.call(f"ifconfig {interface} down", shell=True)
subprocess.call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
subprocess.call(f"ifconfig {interface} up", shell=True)

print("[+] DONE!")
print("-" * 60)