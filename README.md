# MAC Address Changer

A Python CLI tool to change the MAC address of a network interface on Linux — built for educational purposes as part of learning ethical hacking and network security.

---

## Features

- Validates MAC address format before attempting change
- Verifies the interface exists before running
- Confirms whether the MAC address actually changed
- Requires root — exits cleanly with a clear message if not

---

## Requirements

- Linux
- Python 3
- Root privileges
- `net-tools`

```bash
sudo apt install net-tools
```

---

## Usage

```bash
sudo python3 mac_changer.py -i <interface> -m <new_mac>
```

## Options

| Option | Description |
|---|---|
| `-i` / `--Interface` | Network interface (e.g. `eth0`, `wlan0`) |
| `-m` / `--mac` | New MAC address (format: `AA:BB:CC:DD:EE:FF`) |
| `-h` / `--help` | Show help and exit |

---

## Examples

```bash
# Change MAC on eth0
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55

# Change MAC on wlan0
sudo python3 mac_changer.py -i wlan0 -m AA:BB:CC:DD:EE:FF

# See all available interfaces
ifconfig -a
```

---

## How It Works

1. Checks for root privileges
2. Validates the MAC address format (`AA:BB:CC:DD:EE:FF`)
3. Confirms the interface exists
4. Reads and displays the current MAC address
5. Brings the interface down, applies the new MAC, brings it back up
6. Verifies the change was successful

---

## Disclaimer

> For educational purposes only. Use only on devices and networks you own or have explicit permission to test.
