import requests
import time
from deepdiff import DeepDiff
from colorama import init, Fore
import socket

init(convert=True)

# Zeptej se na IP adresu
ip_address = input("Zadejte IP adresu webového serveru (nebo ponechte prázdné pro normální DNS resoluci): ").strip()

# Původní URL
#url = 'https://solana.bool.cz'
url = 'http://404m.com'

# Pokud je zadaná IP adresa, použij ji
if ip_address:
    # Extrahovat hostname z URL
    hostname = url.split("//")[-1].split("/")[0]
    # Sestavit URL s IP adresou a nastavit 'Host' header
    url = url.replace(hostname, ip_address)
    headers = {
        'User-Agent': 'Inteligent Verification Autonomous Network/CyberOS 5.0 (SynthOS NT 10.0; Synth64; x64) CyberCode/537.36 (HyperHTML, like Quantum) Quantum/537.36',
        'Host': hostname
    }
else:
    headers = {
        'User-Agent': 'Inteligent Verification Autonomous Network/CyberOS 5.0 (SynthOS NT 10.0; Synth64; x64) CyberCode/537.36 (HyperHTML, like Quantum) Quantum/537.36'
    }

print(f"Useragent: {Fore.GREEN}{headers}{Fore.RESET}")
print(f"Posílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}HEAD{Fore.RESET}")

start = time.time()

try:
    response = requests.head(url, headers=headers, stream=True, allow_redirects=False, timeout=10)
    json1 = response.headers
    status_1 = response.status_code
    end = time.time()

    print(f"Odpověď z vrátila kód {Fore.CYAN}{status_1}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start), 3)}{Fore.RESET} sekund.")
    print('---- hlavička  ----')
    for key, value in response.headers.items():
        print(f'  {Fore.YELLOW}{key}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}')
    print('------ tělo -------')
    print(f'{Fore.CYAN}{response.text}{Fore.RESET}')

    print(f"Posílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}GET{Fore.RESET}")

    start = time.time()
    response = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
    json2 = response.headers
    status_2 = response.status_code
    end = time.time()

    print(f"Odpověď z vrátila kód {Fore.CYAN}{status_2}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start), 3)}{Fore.RESET} sekund.")
    print('---- hlavička  ----')
    for key, value in response.headers.items():
        print(f'  {Fore.YELLOW}{key}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}')
    print('------ tělo -------')
    vystup = response.text
    vystup = vystup[:100]
    print(f'{Fore.CYAN}{vystup}{Fore.RESET}')
    print('- Rozdíl hlaviček -')

    ddiff = DeepDiff(json1, json2, ignore_order=True)

    if 'dictionary_item_added' in ddiff:
        print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
        for cojejinak in ddiff['dictionary_item_added']:
            klic = cojejinak.split('[')[1].strip(']')
            print(f"{Fore.YELLOW}{klic}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
        print(f"-")

    if 'dictionary_item_removed' in ddiff:
        print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
        for cojejinak in ddiff['dictionary_item_removed']:
            klic = cojejinak.split('[')[1].strip(']')
            print(f"{Fore.YELLOW}{klic}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
        print(f"-")

    if 'values_changed' in ddiff:
        print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
        for cojejinak in ddiff['values_changed']:
            klic = cojejinak.split('[')[1].strip(']')
            print(f"{Fore.YELLOW}{klic}{Fore.RESET}: {Fore.CYAN}{ddiff['values_changed'][cojejinak]['old_value']}{Fore.RESET} -> {Fore.CYAN}{ddiff['values_changed'][cojejinak]['new_value']}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
        print(f"-")

except requests.Timeout:
    print(f'{Fore.RED}Request timeout!{Fore.RESET}')
