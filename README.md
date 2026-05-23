# MAC Address Changer

A Python CLI tool to change the MAC address of a network interface on Linux.

## Features
- MAC address format validation
- Displays current MAC before changing
- Verifies the new MAC after applying

## Usage
```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

## Requirements
- Linux (uses `ifconfig`)
- Root privileges (`sudo`)
- Python 3

## Disclaimer
For educational purposes only. Use on networks you own or have permission to test.
