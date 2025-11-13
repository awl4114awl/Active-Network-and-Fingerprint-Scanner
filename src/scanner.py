"""
scanner.py
Handles network scanning (using Nmap for discovery + Scapy for MAC fallback)
and OS fingerprinting using Nmap.
"""

import nmap
import scapy.all as scapy
from scapy.all import conf

# Force Scapy to use the correct Npcap interface (Index of DisplayLink adapter)
conf.iface = 7

# Improve capture reliability on Windows
conf.use_pcap = True
conf.sniff_promisc = True


def scan_network(ip_range: str):
    """
    Discover hosts using Nmap (-sn ping/ARP scan).
    Then resolve MAC addresses using:
        1. Nmap's MAC (if available)
        2. Scapy ARP request (fallback)
    Returns:
        [{'ip': str, 'mac': str}]
    """
    devices = []

    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=ip_range, arguments='-sn')

        for host in nm.all_hosts():

            # 1. MAC from Nmap (best case)
            mac = nm[host]["addresses"].get("mac", None)

            # 2. MAC fallback using Scapy
            if not mac:
                ans, _ = scapy.srp(
                    scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=host),
                    timeout=1,
                    verbose=False
                )
                mac = ans[0][1].hwsrc if ans else "Unknown"

            devices.append({
                "ip": host,
                "mac": mac
            })

    except Exception as e:
        print(f"[ERROR] Network scan failed: {e}")

    return devices


def fingerprint_device(ip: str) -> str:
    """
    Fingerprint an OS using Nmap's aggressive OS detection.
    Returns:
        "Name (accuracy%)"
        or "Unknown"
    """
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments="-O --osscan-guess --fuzzy")

        os_matches = nm[ip].get("osmatch", [])
        if not os_matches:
            return "Unknown"

        best = max(os_matches, key=lambda x: int(x.get("accuracy", 0)))
        name = best.get("name", "Unknown")
        accuracy = best.get("accuracy", 0)

        return f"{name} ({accuracy}% accurate)"

    except Exception:
        return "Unknown"
