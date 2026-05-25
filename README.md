# MAC Address Changer

A Python CLI tool to change, randomize, restore, and track MAC addresses on Linux network interfaces. Built as part of learning ethical hacking and network security.

---

## Features

- Change MAC address to a custom value
- Generate a random MAC address with one flag
- Restore the previous MAC address from backup
- Stealth mode — auto-randomizes MAC every N minutes
- Full history log with timestamps, interface, old and new MAC
- Input validation — MAC format, interface existence, root check

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
sudo python3 mac_changer.py -i <interface> [option]
```

## Options

| Option | Description |
|---|---|
| `-i` / `--Interface` | Network interface (e.g. `eth0`, `wlan0`) |
| `-m` / `--mac` | Set a custom MAC address |
| `-r` / `--random` | Generate and apply a random MAC address |
| `-e` / `--restore` | Restore the previously saved MAC address |
| `-s` / `--Stealth` | Stealth mode — change MAC every N minutes |
| `-H` / `--history` | View MAC change history with timestamps |
| `--help` | Show help and exit |

---

## Examples

```bash
# Set a custom MAC
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55

# Generate a random MAC
sudo python3 mac_changer.py -i eth0 -r

# Restore previous MAC
sudo python3 mac_changer.py -i eth0 -e

# Stealth mode — change every 5 minutes
sudo python3 mac_changer.py -i eth0 -s 5

# View history
sudo python3 mac_changer.py -H

# See available interfaces
ifconfig -a
```

---

## How It Works

1. Checks for root privileges
2. Validates MAC format and interface existence
3. Saves current MAC to `~/.mac_changer_backup` before changing
4. Brings interface down, applies new MAC, brings it back up
5. Verifies the change was successful
6. Logs every change to `~/.Mac_Address_History` with timestamp

---

## File Storage

| File | Purpose |
|---|---|
| `~/.mac_changer_backup` | Stores last MAC for restore |
| `~/.Mac_Address_History` | Full log of all MAC changes |

---

## Disclaimer

> For educational purposes only. Use only on devices and networks you own or have explicit permission to test.
