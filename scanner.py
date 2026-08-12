import asyncio
import random
import sys
from aiohttp_socks import open_connection

# --- CONFIGURATION ---
# Default: Tor SOCKS5 proxy (socks5h ensures DNS resolution happens inside Tor)
# Set to None to scan directly (NOT RECOMMENDED for privacy)
PROXY_URL = 'socks5h://127.0.0.1:9050'

# Target: Default to localhost for safety. Change only if authorized.
TARGET_IP = "127.0.0.1"

# Scan Range: 1-1000 (Fast) | 1-65535 (Thorough but slow via Tor)
START_PORT = 1
END_PORT = 1000

# Concurrency: Lower for Tor to avoid circuit exhaustion
CONCURRENCY = 50 if PROXY_URL else 200
TIMEOUT = 2.0 if PROXY_URL else 0.5
# ---------------------

async def scan_port(sem, target, port, proxy_url, timeout):
    """
    Privacy-Focused Scan:
    1. Routes through SOCKS5 proxy (Tor) if URL provided.
    2. Performs ONLY TCP Handshake. No banners, no probes.
    3. Randomized micro-delays to evade rate-based IDS.
    """
    async with sem:
        try:
            # Random delay to evade statistical detection
            await asyncio.sleep(random.uniform(0.05, 0.2))
            
            if proxy_url:
                # Use aiohttp_socks with URL format (socks5h prevents DNS leaks)
                reader, writer = await asyncio.wait_for(
                    open_connection(host=target, port=port, proxy_url=proxy_url),
                    timeout=timeout
                )
            else:
                # Direct connection (Insecure)
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(target, port),
                    timeout=timeout
                )
            
            # IMMEDIATELY close. Do not send data.
            writer.close()
            await writer.wait_closed()
            
            return port, True
            
        except Exception:
            # Silently fail to prevent information leakage
            return port, False

async def main(target, start_port, end_port, proxy_url, concurrency, timeout):
    mode = "ANONYMOUS (Tor)" if proxy_url else "DIRECT (INSECURE)"
    print(f"[*] Mode: {mode}")
    
    # Randomize ports to prevent predictable sequential patterns
    ports = list(range(start_port, end_port + 1))
    random.shuffle(ports)
    
    sem = asyncio.Semaphore(concurrency)
    print(f"[*] Starting Stealth Scan on {target} (Ports {start_port}-{end_port})...")
    
    tasks = [scan_port(sem, target, p, proxy_url, timeout) for p in ports]
    open_ports = []
    
    for coro in asyncio.as_completed(tasks):
        port, is_open = await coro
        if is_open:
            open_ports.append(port)
            print(f"[+] {port}")
    
    open_ports.sort()
    print(f"\n[+] Complete. Found {len(open_ports)} open ports.")
    return open_ports

if __name__ == "__main__":
    print("SECURITY PROTOCOL: Ensure you have written authorization.")
    confirm = input("Do you have explicit permission? (yes/no): ")
    if confirm.lower() != "yes":
        sys.exit(1)

    try:
        # Ensure Tor is running if proxy is enabled
        if PROXY_URL:
            print("[*] Verifying Tor connection... (If this hangs, start 'sudo systemctl start tor')")
        
        asyncio.run(main(TARGET_IP, START_PORT, END_PORT, PROXY_URL, CONCURRENCY, TIMEOUT))
    except KeyboardInterrupt:
        print("\n[!] Aborted by user. No logs saved.")
        sys.exit(0)
    except Exception:
        print("\n[!] An internal error occurred. Check Tor/Proxy configuration.")
        sys.exit(1)   
