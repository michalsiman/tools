import requests
import time
import subprocess
import platform
from datetime import datetime

# Seznam monitorovaných IP adres a názvů webů
sites = [
    {"ip": "8.8.8.8", "name": "Google DNS"},
    {"ip": "1.1.1.1", "name": "Cloudflare DNS"},
    {"ip": "192.168.1.1", "name": "Local Router"}
]

# URL ntfy (přizpůsob si topic)
ntfy_url = "https://ntfy.sh/yourownname"

# Interval kontroly (v sekundách)
INTERVAL = 900  # Výchozí 5 minut (300 sekund)

def is_online(ip):
    """Pingne IP a vrátí True, pokud je dostupná, jinak False"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Chyba při pingování {ip}: {e}")
        return False

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Provede kontrolu dostupnosti
    print(f"\n[{now}] Probíhá kontrola:")
    
    for site in sites:
        ip, name = site["ip"], site["name"]
        
        if not is_online(ip):
            print(f"❌ {ip} - {name} je nedostupný!")
            requests.post(ntfy_url, data=f"⚠️ {name} ({ip}) je offline!")
        else:
            print(f"✅ {ip} - {name} je dostupný.")
    
    # Zobrazení informace o další kontrole
    print(f"⏳ Další kontrola za {INTERVAL // 60} minut.")
    
    # Pauza před další kontrolou
    time.sleep(INTERVAL)
