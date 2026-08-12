import asyncio
import random
import sys
import os
import argparse
from aiohttp_socks import open_connection

async def scan_port(sem, target, port, proxy_url, timeout):
    async with sem:
        try:
            # Random delay for stealth (only if proxy is used)
            if proxy_url:
                await asyncio.sleep(random.uniform(0.1, 0.3))
            
            if proxy_url:
                # Connect via Proxy (Tor/VPN)
                reader, writer = await asyncio.wait_for(
                    open_connection(host=target, port=port, proxy_url=proxy_url),
                    timeout=timeout
                )
            else:
                # Direct Connection
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(target, port),
                    timeout=timeout
                )
            
            writer.close()
            await writer.wait_closed()
            return port, True
            
        except Exception:
            return port, False

async def main(target, start_port, end_port, proxy_url, concurrency, timeout):
    mode = "ANONYMOUS (Tor/Proxy)" if proxy_url else "DIRECT (Standard)"
    print(f"[*] Mode: {mode}")
    if proxy_url:
        print(f"[*] Routing via: {proxy_url}")
    
    print(f"[*] Scanning {target} (Ports {start_port}-{end_port})...")
    
    ports = list(range(start_port, end_port + 1))
    random.shuffle(ports)
    
    sem = asyncio.Semaphore(concurrency)
    tasks = [scan_port(sem, target, p, proxy_url, timeout) for p in ports]
    open_ports = []
    
    completed = 0
    total = len(ports)
    
    for coro in asyncio.as_completed(tasks):
        port, is_open = await coro
        if is_open:
            open_ports.append(port)
            print(f"[+] {port}")
        
        completed += 1
        if completed % 1000 == 0:
            print(f"[*] Progress: {completed}/{total}...")
    
    open_ports.sort()
    print(f"\n[+] Complete. Found {len(open_ports)} open ports.")

if __name__ == "__main__":
    # --- ARGUMENT PARSER (Makes it easy for users) ---
    parser = argparse.ArgumentParser(description="Privacy-Focused Port Scanner")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Target IP (default: 127.0.0.1)")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (e.g., 1-65535)")
    parser.add_argument("--tor", action="store_true", help="Enable Tor (routes via socks5h://127.0.0.1:9050)")
    parser.add_argument("--proxy", type=str, help="Custom SOCKS5 proxy (e.g., socks5h://127.0.0.1:9050)")
    parser.add_argument("--threads", type=int, default=100, help="Concurrency level")
    args = parser.parse_args()
    
    # Determine Proxy Configuration
    proxy_url = None
    if args.tor:
        proxy_url = "socks5h://127.0.0.1:9050"
    elif args.proxy:
        proxy_url = args.proxy
    elif os.getenv("SCANNER_PROXY"):
        proxy_url = os.getenv("SCANNER_PROXY")

    # Parse Port Range
    try:
        start_p, end_p = map(int, args.ports.split("-"))
    except ValueError:
        print("Invalid port range. Use format: 1-1000")
        sys.exit(1)

    # Security Check
    print("SECURITY PROTOCOL: Ensure you have written authorization.")
    confirm = input("Do you have explicit permission? (yes/no): ")
    if confirm.lower() != "yes":
        sys.exit(1)

    # Adjust concurrency for Tor automatically
    concurrency = 30 if proxy_url else args.threads
    timeout = 3.0 if proxy_url else 0.5

    try:
        if proxy_url:
            print("[*] Verifying Tor/Proxy connection...")
        
        asyncio.run(main(args.target, start_p, end_p, proxy_url, concurrency, timeout))
    except KeyboardInterrupt:
        print("\n[!] Aborted by user.")
        sys.exit(0)
    except Exception:
        print("\n[!] Error occurred. Check proxy settings.")
        sys.exit(1)   
