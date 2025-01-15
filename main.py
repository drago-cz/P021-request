# Skript, bude posílat requesty na URL a měřit odezvu 
"""
TO DO:
- ošetření timeoutu
- přidání nějakých dalších informací jako je IP adresa
"""
import requests
import time
from deepdiff import DeepDiff
from colorama import init, Fore
from urllib.parse import urlparse
import socket
import ipaddress

# Inicializace colorama s automatickým resetem barev
init(convert=True)

headers = {
    'User-Agent': 'Inteligent Verification Autonomous Network/CyberOS 5.0 (SynthOS NT 10.0; Synth64; x64) CyberCode/537.36 (HyperHTML, like Quantum) Quantum/537.36',
    'Accept-Language': 'en-US;q=0.8,en;q=0.7'
}

print(f"Useragent: {Fore.GREEN}{headers}{Fore.RESET}")

# Ověří, zda je zadaná URL platná.
# Podmínky:
# Musí obsahovat platný schéma (http nebo https)
# Musí obsahovat platnou doménu (netloc)
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and bool(parsed.netloc)
    except Exception:
        return False

# Tato funkce opakovaně žádá uživatele o zadání URL, dokud není zadána platná URL podle funkce is_valid_url.
# Pokud uživatel zadá neplatnou URL, zobrazí se červené varování a požádá se o opětovné zadání.
def get_valid_url():
    while True:
        url = input("Zadejte URL kterou prověříme (nebo 'exit' pro ukončení): ").strip()
        if url.lower() == 'exit':
            print("Ukončuji skript.")
            exit(0)
        if is_valid_url(url):
            return url
        else:
            print(f"{Fore.RED}Neplatná URL. Prosím, zkuste to znovu.{Fore.RESET}")

# Tato funkce validuje IP adresu
# Vrací buď validní IP adresu, nebo False, pokud je prázdná
def get_and_validate_ip():
    while True:
        ip = input("Zadej IP adresu, kde má doména být (origin server), anebo nech prázdné pro získání IP z DNS: ").strip()
        # Pokud je prázdná, vrátí False
        if ip == '':
            return False
        # ukončení skriptu pokud zadá exit
        if ip.lower() == 'exit':
            print("Ukončuji skript.")
            exit(0)

        try:
            # Otestuje IP adresu
            ipaddress.ip_address(ip)
            # Pokud je validní, vrátí ji
            return ip
        except ValueError:
            # Jinak vypíše chybu a nechá uživatele opakovat
            print(f"{Fore.RED}Neplatná IP adresa. Prosím, zkuste to znovu.{Fore.RESET}")


# Vytiskne hlavičky s zarovnáním hodnot.
def print_headers(headers_dict):
    if not headers_dict:
        print(f"{Fore.YELLOW}Žádné hlavičky k zobrazení.{Fore.RESET}")
        return

    # Zjistíme maximální délku klíče pro zarovnání
    max_key_length = max(len(key) for key in headers_dict.keys())

    for key, value in headers_dict.items():
        print(f"  {Fore.YELLOW}{key:<{max_key_length}}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}")


#  blok try-except pro ošetření případných výjimek při odesílání HTTP requestů, což zajistí, že skript nebude přerušen neočekávanou chybou a uživatel dostane informaci o tom, co se pokazilo.
while True:
    url = get_valid_url()
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    origin_ip = get_and_validate_ip()

    # Pokus o vyřešení IP adresy hostitele pokud není zadána origin IP
    if origin_ip == False:
        try:
            ip_address = socket.gethostbyname(host)
            print(f"{Fore.GREEN}IP adresa pro {host} (získáno z DNS): {ip_address}{Fore.RESET}")
        except socket.gaierror:
            print(f"{Fore.RED}Chyba: Nelze resolvovat IP adresu pro hostitele '{host}'.{Fore.RESET}")
            print("\n--- Nemá cenu posílat další (jiné) requesty ---\n")
            continue  # Přeskočí GET request a pokračuje s další URL

    # TODO else pro zpracování origin IP

    # TODO upravit request aby šel na IP adresu webserveru

    # Odesílání HEAD requestu
    try:
        print(f"\nPosílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}HEAD{Fore.RESET}")
        start = time.time()

        response_head = requests.head(url, headers=headers, allow_redirects=False, timeout=10)
        json1 = response_head.headers
        status_1 = response_head.status_code
        end = time.time()

        print(f"Odpověď vrátila kód {Fore.CYAN}{status_1}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
        print('---- hlavička  ----')
        print_headers(response_head.headers)
        print('------ tělo -------')
        if response_head.text:
            print(f'{Fore.CYAN}{response_head.text}{Fore.RESET}')
        else:
            print(f"{Fore.YELLOW}Žádné tělo odpovědi.{Fore.RESET}")

    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Chyba připojení. Nelze se připojit k {host} ({ip_address}). Cílový server neodpovídá.{Fore.RESET}")
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Vypršel časový limit při připojování k {host} ({ip_address}).{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Došlo k chybě při odesílání HEAD requestu: {e}{Fore.RESET}")

    # Odesílání GET requestu
    try:
        print(f"\nPosílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}GET{Fore.RESET}")
        start = time.time()

        response_get = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
        json2 = response_get.headers
        status_2 = response_get.status_code
        end = time.time()

        print(f"Odpověď vrátila kód {Fore.CYAN}{status_2}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
        print('---- hlavička  ----')
        print_headers(response_get.headers)
        print('------ tělo -------')
        vystup = response_get.text[:100]
        print(f'{Fore.CYAN}{vystup}{Fore.RESET}')
        print('- Rozdíl hlaviček -')

        ddiff = DeepDiff(json1, json2, ignore_order=True)

        # Zpracování 'dictionary_item_added'
        if 'dictionary_item_added' in ddiff:
            added_keys = [key.split('[')[1].strip(']') for key in ddiff['dictionary_item_added']]
            max_key_length_added = max(len(key) for key in added_keys) if added_keys else 0
            print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
            for klic in added_keys:
                print(f"  {Fore.YELLOW}{klic:<{max_key_length_added}}{Fore.RESET}")
        else:
            print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
            print(f"-")

        # Zpracování 'dictionary_item_removed'
        if 'dictionary_item_removed' in ddiff:
            removed_keys = [key.split('[')[1].strip(']') for key in ddiff['dictionary_item_removed']]
            max_key_length_removed = max(len(key) for key in removed_keys) if removed_keys else 0
            print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
            for klic in removed_keys:
                print(f"  {Fore.YELLOW}{klic:<{max_key_length_removed}}{Fore.RESET}")
        else:
            print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
            print(f"-")

        # Zpracování 'values_changed'
        if 'values_changed' in ddiff:
            print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
            for key, change in ddiff['values_changed'].items():
                klic = key.split('[')[1].strip(']')
                old_val = change['old_value']
                new_val = change['new_value']
                print(f"  {Fore.YELLOW}{klic}{Fore.RESET}: {Fore.CYAN}{old_val}{Fore.RESET} -> {Fore.CYAN}{new_val}{Fore.RESET}")
        else:
            print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
            print(f"-")

    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Chyba připojení. Nelze se připojit k {host} ({ip_address}). Cílový server neodpovídá.{Fore.RESET}")
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Vypršel časový limit při připojování k {host} ({ip_address}).{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Došlo k chybě při odesílání GET requestu: {e}{Fore.RESET}")

    print("\n--- Další URL ---\n")