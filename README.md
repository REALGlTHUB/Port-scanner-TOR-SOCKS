# 🔒 Anonymous Port Scanner (Tor/SOCKS5)

A high-speed, asynchronous port scanner designed for privacy. It supports routing traffic through **Tor** or custom **SOCKS5 proxies** to hide your identity.

> ⚠️ **PREREQUISITE FOR ANONYMOUS SCANNING**
> To use the `--tor` feature, you **MUST** have the Tor service installed and running on your machine.
> *   **Linux (Debian/Ubuntu):** `sudo apt install tor` then `sudo systemctl start tor`
> *   **Windows/Mac:** You must run the **Tor Browser** or **Tor Daemon** in the background before scanning.
> *   **No Tor?** You can still use this tool with a custom SOCKS5 proxy (see Usage #3) or in direct mode (not anonymous).

## 🚀 Installation

You need Python 3.10+ and the following libraries:

```bash
pip install aiohttp-socks python-socks[asyncio]   
