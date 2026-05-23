#!/usr/bin/env python

import subprocess 
import optparse

def get_arguments():
    parse = optparse.OptionParser()

    parse.add_option("-i", "--Interface", dest="INTERFACE", help="Enter the Interface name to change it")
    parse.add_option("-m", "--mac", dest="MAC_ADDRESS", help="Enter your custom mac address")

    (options, arguments) = parse.parse_args()
    
    if not options.INTERFACE:
        parse.error("[-] Kindly enter a interface name or use --help")
    elif not options.MAC_ADDRESS:
        parse.error("[-] kindly enter the mac address or use --help")
    else:
        return options.INTERFACE, options.MAC_ADDRESS



def change_mac_address(interface, mac):
    print("-" * 60)
    current_mac = subprocess.check_output(
       f"ifconfig {interface} | grep ether | awk '{{print $2}}'",
       shell= True
    )
    c_m = current_mac.decode("utf-8").strip()
    print(f"[+] Your current mac address: {c_m}")
    print(f"[+] changing MAC address for {interface} to {mac}")

    try:
     subprocess.check_call(["ifconfig", interface, "down"])
     subprocess.check_call(["ifconfig", interface, "hw", "ether", mac])
     subprocess.check_call(["ifconfig", interface, "up"])

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
    
