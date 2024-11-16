# Active Network and Fingerprint Scanner

A simple network scanner with a graphical user interface (GUI) built using Python and Tkinter. This tool scans a specified IP range to discover devices on the network, displaying their IP addresses, MAC addresses, and operating systems.

## Features
- **Network Discovery**: Scan a range of IP addresses to find active devices.
- **OS Fingerprinting**: Identify the operating system of detected devices.
- **Modern GUI**: Responsive and user-friendly interface with a sleek dark mode.
- **Dynamic Scrollbar**: Only appears when the results exceed the visible area.
- **Progress Bar**: Displays scan progress in real-time.

## Requirements
- **Python 3.x**
- **Dependencies**:
  - `scapy` for network scanning
  - `python-nmap` for OS fingerprinting
  - `tkinter` for GUI

### Installation on Fedora
1. Install Python and necessary libraries:
   ```bash
   sudo dnf install python3 python3-tkinter
   pip install scapy python-nmap
   ```

2. Install Nmap:
   ```bash
   sudo dnf install nmap
   ```

3. Clone the repository:
   ```bash
   git clone git@github.com:awl4114awl/Active-Network-and-Fingerprint-Scanner.git
   cd Active-Network-and-Fingerprint-Scanner
   ```

## Usage
1. Run the application:
   ```bash
   python3 network_scanner.py
   ```

2. Enter the IP range (e.g., `192.168.1.0/24`) and click the "Scan" button.

3. View the discovered devices in the table. The IP, MAC, and OS details will be displayed.

## Example Output
- **Table View**:
  ```
  +----------------+-------------------+---------------------------+
  | IP Address     | MAC Address       | Operating System          |
  +----------------+-------------------+---------------------------+
  | 192.168.1.1    | 88:DE:7C:C7:88:10 | Linux 3.11 - 4.1 (96%)    |
  | 192.168.1.86   | 00:0C:43:8B:97:95 | Unknown                   |
  +----------------+-------------------+---------------------------+
  ```

- **Progress Bar**:
  A progress bar at the bottom of the interface indicates scanning progress.

## Contributions
Contributions are welcome! If you encounter any issues or have suggestions for improvement, feel free to submit an issue or pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


