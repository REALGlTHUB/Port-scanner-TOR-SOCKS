# 🔒 Anonymous Port Scanner (Tor/SOCKS5)

A high-speed, asynchronous port scanner designed for privacy. It supports routing traffic through **Tor** or custom **SOCKS5 proxies** to hide your identity.

> ⚠️ **PREREQUISITE FOR ANONYMOUS SCANNING**
> To use the `--tor` feature, you **MUST** have the Tor service installed and running on your machine.
> *   **Linux (Debian/Ubuntu):** `sudo apt install tor` then `sudo systemctl start tor`
> *   **Windows/Mac:** You must run the **Tor Browser** or **Tor Daemon** in the background before scanning.
> *   **No Tor?** You can still use this tool with a custom SOCKS5 proxy (see Usage #3) or in direct mode (not anonymous).

## 🚀 Installation & Quick Start

### Option A: Automatic Terminal Install (Recommended)
*This method downloads, extracts, and sets up everything in one go. No "file not found" errors.*

1.  **Open Terminal** and run this single command:
    ```bash
    wget https://github.com/REALGlTHUB/Port-scanner-TOR-SOCKS/archive/refs/heads/main.zip -O scanner.zip && unzip scanner.zip && cd Port-scanner-TOR-SOCKS-main && rm scanner.zip
    ```
    *(Note: If `wget` or `unzip` is missing, install them with `sudo apt install wget unzip -y`)*

2.  **Install System Dependencies** (Required for Debian 13/Qubes/Ubuntu 24.04+):
    ```bash
    sudo apt update
    sudo apt install python3-venv -y
    ```

3.  **Create & Activate Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(You will see `(venv)` appear in your prompt).*

4.  **Install Tool Dependencies**:
    ```bash
    pip install aiohttp-socks python-socks[asyncio]
    ```

5.  **Run the Scanner**:
    ```bash
    python scanner.py --tor
    ```

---

### Option B: Manual Download (GUI)
1.  Click the green **<> Code** button > **Download ZIP**.
2.  **Unzip** the folder.
3.  **Open Terminal** inside the extracted folder (Right-click > "Open Terminal Here" or `cd` into it).
4.  Follow **Steps 2-5** from Option A above.   

## 📖 Usage Guide

### 1. Run with Tor (Anonymous)
*Hides your IP. Requires Tor to be running.*
```bash
python scanner.py --tor

2. Change Target IP
Scan a specific device (e.g., your router or a server).

python scanner.py --tor -t 192.168.1.50

3. Scan All Ports
Scans ports 1 to 65535. Note: This is slower via Tor.

python scanner.py --tor -p 1-65535

4. Use Custom SOCKS5 Proxy
If you don't have Tor but have a proxy (e.g., from a VPN).

python scanner.py --proxy socks5h://127.0.0.1:9050

5. Direct Scan (No Proxy)
Fastest mode, but your IP is visible.

python scanner.py

⚙️ Advanced Options
Command	Description	Example
-t, --target	Set target IP	-t 10.0.0.5
-p, --ports	Set port range	-p 1-65535
--tor	Enable Tor routing	--tor
--proxy	Custom SOCKS5 URL	--proxy socks5h://...
--threads	Set concurrency	--threads 50

Full Example: Scan all ports on 192.168.1.1 using Tor:

python scanner.py --tor -t 192.168.1.1 -p 1-65535

⚖️ Legal Disclaimer & Responsibility
This tool is provided for educational and authorized security testing purposes only.

Authorization: You must have explicit written permission from the owner of any network or device you scan.
No Liability: The developers are not responsible for any misuse, damages, legal issues, or network disruptions caused by this software.
Compliance: Users are solely responsible for complying with all applicable laws (e.g., CFAA, Computer Misuse Act).
Usage: By using this tool, you acknowledge that you are fully responsible for your actions.
🛡️ Privacy Features
DNS Leak Protection: Uses socks5h to resolve domains inside the Tor network.
No Logs: Results are printed to screen only; nothing is saved to disk.
Stealth Mode: Randomized delays and port ordering to evade detection.
