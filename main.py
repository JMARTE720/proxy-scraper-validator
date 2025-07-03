// proxy_scraper_validator/main.py
import os
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# === CONFIGURACIÓN DE CARPETA LOCAL ===
OUTPUT_DIR = os.path.join(os.getcwd(), "proxies")

# === FUNCIONES BASE ===
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📂 Carpeta creada: {folder_path}")

def append_proxy_if_new(file_path, proxy):
    create_folder_if_not_exists(OUTPUT_DIR)
    full_path = os.path.join(OUTPUT_DIR, file_path)
    existing = set()
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            existing = set(line.strip() for line in f)
    if proxy not in existing:
        with open(full_path, 'a') as f:
            f.write(proxy + '\n')
        return True
    return False

def test_proxy(proxy, proxy_type):
    try:
        proxies = {
            'http': f'{proxy_type}://{proxy}',
            'https': f'{proxy_type}://{proxy}'
        }
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=6)
        return r.status_code == 200
    except:
        return False

def validate_proxy_batch(proxies):
    valid_count = 0
    file_map = {"http": "http.txt", "socks4": "socks4.txt", "socks5": "socks5.txt"}

    def detect_and_save(proxy):
        for tipo in ["http", "socks4", "socks5"]:
            if test_proxy(proxy, tipo):
                if append_proxy_if_new(file_map[tipo], proxy):
                    return 1
                break
        return 0

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(detect_and_save, p) for p in proxies]
        for future in as_completed(futures):
            valid_count += future.result()

    return valid_count

def scrape_and_validate_from(urls):
    headers = {'User-Agent': 'Mozilla/5.0'}
    total_valid = 0
    for url in urls:
        print(f"🌐 Visitando: {url}")
        try:
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
            proxies = re.findall(r'\d{1,3}(?:\.\d{1,3}){3}:\d{2,5}', r.text)
            unique_proxies = list(set(proxies))
            print(f"🔍 Extraídos {len(unique_proxies)} proxies únicos")
            valid_count = validate_proxy_batch(unique_proxies)
            total_valid += valid_count
            print(f"✅ Válidos desde {url}: +{valid_count}")
        except Exception as e:
            print(f"❌ Error en {url}: {e}")
    return total_valid

if __name__ == "__main__":
    urls = [
        'https://www.free-proxy-list.net/',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/main/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt'
    ]

    modo = input("Modo:
1. Ejecutar una vez
2. Ejecutar en bucle
Opción (1/2): ")
    loop = modo.strip() == "2"

    while True:
        total = scrape_and_validate_from(urls)
        print(f"🎯 Total proxies válidos nuevos: {total}")
        if not loop:
            break
        time.sleep(10)
