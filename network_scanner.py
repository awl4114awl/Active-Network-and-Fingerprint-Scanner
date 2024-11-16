import tkinter as tk
from tkinter import ttk
import threading
import scapy.all as scapy
import nmap

def scan_network(ip_range):
    """
    Scans the network for active devices using ARP requests.
    """
    devices = []
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered_list = scapy.srp(broadcast / arp_request, timeout=1, verbose=False)[0]
    for element in answered_list:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return devices

def fingerprint_device(ip):
    """
    Fingerprints the OS of a device using Nmap.
    """
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-O --osscan-guess --fuzzy')
    try:
        os_matches = nm[ip]['osmatch']
        if os_matches:
            best_match = max(os_matches, key=lambda x: int(x['accuracy']))
            return f"{best_match['name']} ({best_match['accuracy']}% accurate)"
    except:
        pass
    return "Unknown"

def start_scan_thread():
    """
    Starts the scan in a separate thread.
    """
    scan_button.config(state="disabled")
    threading.Thread(target=start_scan, daemon=True).start()

def start_scan():
    """
    Performs the scan and updates the GUI.
    """
    for row in tree.get_children():
        tree.delete(row)

    ip_range = ip_entry.get()
    devices = scan_network(ip_range)
    for device in devices:
        os = fingerprint_device(device['ip'])
        tree.insert("", "end", values=(device['ip'], device['mac'], os))
    
    # Adjust scrollbar visibility
    update_scrollbar_visibility()

    scan_button.config(state="normal")

def update_scrollbar_visibility():
    """
    Show or hide the scrollbar based on the number of rows in the Treeview.
    """
    if len(tree.get_children()) > 10:  # Arbitrary threshold for scrollbar visibility
        scrollbar.pack(side="right", fill="y")
    else:
        scrollbar.pack_forget()

# Create the main application window
root = tk.Tk()
root.title("Network Scanner")

# Set up dark mode styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#333333", foreground="white", rowheight=25, fieldbackground="#333333")
style.map("Treeview", background=[("selected", "#666666")])
style.configure("TButton", background="#444444", foreground="white", borderwidth=1)
style.map("TButton", background=[("active", "#555555")])
style.configure("TEntry", background="#333333", foreground="white", fieldbackground="#333333")
style.configure("TLabel", background="#222222", foreground="white")
style.configure("TFrame", background="#222222")

# Set the background color for the main window
root.configure(bg="#222222")

# Input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")
ttk.Label(input_frame, text="IP Range:").pack(side="left", padx=5)
ip_entry = ttk.Entry(input_frame, width=20)
ip_entry.pack(side="left", padx=5)
scan_button = ttk.Button(input_frame, text="Scan", command=start_scan_thread)
scan_button.pack(side="left", padx=5)

# Results table
columns = ("IP Address", "MAC Address", "Operating System")
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")
tree.pack(pady=10, padx=10, fill="both", expand=True)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Initially hide the scrollbar
update_scrollbar_visibility()

# Run the application
root.mainloop()

