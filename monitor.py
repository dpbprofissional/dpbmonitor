import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SURFACE_SOURCES = [
    "https://pastebin.com/archive",
    "https://paste.ee/recent"
]

def monitor_surface():
    for url in SURFACE_SOURCES:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        print(f"[{datetime.utcnow()}] Monitorando {url}")

while True:
    monitor_surface()
    time.sleep(1800)  # a cada 30 minutos