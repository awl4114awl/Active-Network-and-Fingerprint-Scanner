# 🛰️ Active Network & Fingerprint Scanner

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-Networking-yellow?style=for-the-badge)
![Nmap](https://img.shields.io/badge/Nmap-OS%20Fingerprinting-orange?style=for-the-badge&logo=nmap)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-9cf?style=for-the-badge)
![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows11)
![Status](https://img.shields.io/badge/Project-Active-success?style=for-the-badge)

A modern Python application that performs **ARP-based network discovery** and **OS fingerprinting** using Nmap.  
This tool identifies active hosts on a subnet, retrieves their MAC addresses, and estimates operating systems using Nmap’s detection engine — all through a clean, dark-mode Tkinter GUI.

---

## 📸 Screenshot

<p align="left">
  <img src="screenshots/Screenshot 2025-11-13 141951.png" width="500">
 <img src="screenshots/Screenshot 2025-11-13 141917.png" width="500">
</p>

---

## ⚡ Features

### ✔ ARP-Based Network Scanning
- Discovers live hosts using Scapy ARP sweeps  
- Displays IP + MAC for each responding device

### ✔ OS Fingerprinting (Nmap)
- Uses: `nmap -O --osscan-guess --fuzzy`
- Identifies OS families, versions, and accuracy %

### ✔ Clean Dark-Mode User Interface
- Fixed 600×400 layout  
- Balanced columns  
- Scrollbar always visible  
- Buttons disable during scan to prevent thread conflicts

### ✔ User Experience Improvements
- Background thread scanning (no frozen UI)
- Progress bar + status footer
- “Ready”, “Scanning…”, “X devices found”
- CSV export option

---

## 🗂 Project Structure

```

Active-Network-and-Fingerprint-Scanner/
│
├── src/
│   ├── __init__.py
│   ├── scanner.py          # Network scanning + fingerprinting logic
│   ├── gui.py              # All Tkinter UI logic
│
├── screenshots/        # App screenshots for README)
│
├── tests/
│   ├── test_scanner.py     # Unit tests (basic)
│
├── requirements.txt
├── README.md
├── LICENSE
└── run.py                  # Launches the GUI
````
---

## 🚀 Installation & Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
````

### 2. Install Nmap (required)

Download for Windows:
[https://nmap.org/download.html#windows](https://nmap.org/download.html#windows)

Enable: **Add Nmap to PATH**

### 3. Install Npcap (required)

Download:
[https://npcap.com/](https://npcap.com/)

Enable: **WinPcap compatibility mode**

### 4. Run the app

```bash
python run.py
```

---

## 🔧 Technical Overview

### **Device Discovery (ARP Sweep)**

Uses a broadcast ARP request:

```python
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
```

Hosts that respond are considered active.

### **OS Fingerprinting**

Runs:

```
nmap -O --osscan-guess --fuzzy <ip>
```

Parses:

* OS matches
* Accuracy values
* Best match selection

---

## 📤 CSV Export

Exports all discovered devices with:

| IP Address | MAC Address | Operating System |
| ---------- | ----------- | ---------------- |

---

## 🛡 Disclaimer

Use this tool **only on networks you own or have explicit permission to scan**.
Unauthorized scanning may violate laws or policies.

---

## ⭐ Future Enhancements

* Multi-threaded OS scanning (faster scans)
* Network interface selection
* ICMP/TCP fallback for ARP-hidden devices
* Build as standalone `.exe`
* Integrated log window

---
