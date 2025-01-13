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
        url = input("Zadejte URL kterou prověříme: ").strip()
        if is_valid_url(url):
            return url
        else:
            print(f"{Fore.RED}Neplatná URL. Prosím, zkuste to znovu.{Fore.RESET}")

# Vytiskne hlavičky s zarovnáním hodnot.
def print_headers(headers_dict):
    if not headers_dict:
        print(f"{Fore.YELLOW}Žádné hlavičky k zobrazení.{Fore.RESET}")
        return

    # Zjistíme maximální délku klíče pro zarovnání
    max_key_length = max(len(key) for key in headers_dict.keys())

    for key, value in headers_dict.items():
        print(f"  {Fore.YELLOW}{key:<{max_key_length}}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}")


url = get_valid_url()

#  blok try-except pro ošetření případných výjimek při odesílání HTTP requestů, což zajistí, že skript nebude přerušen neočekávanou chybou a uživatel dostane informaci o tom, co se pokazilo.
try:
    print(f"\nPosílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}HEAD{Fore.RESET}")
    start = time.time()

    response_head = requests.head(url, headers=headers, stream=True, allow_redirects=True)
    json1 = response_head.headers
    status_1 = response_head.status_code
    end = time.time()

    print(f"Odpověď z vrátila kód {Fore.CYAN}{status_1}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
    print('---- hlavička  ----')
    print_headers(response_head.headers)
    print('------ tělo -------')
    # HEAD request obvykle nevrací tělo, ale pokud ano, vypíšeme ho
    if response_head.text:
        print(f'{Fore.CYAN}{response_head.text}{Fore.RESET}')
    else:
        print(f"{Fore.YELLOW}Žádné tělo odpovědi.{Fore.RESET}")

    # ------------

    print(f"\nPosílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}GET{Fore.RESET}")
    start = time.time()

    response_get = requests.get(url, headers=headers, allow_redirects=True)
    json2 = response_get.headers
    status_2 = response_get.status_code
    end = time.time()

    print(f"Odpověď z vrátila kód {Fore.CYAN}{status_2}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
    print('---- hlavička  ----')
    print_headers(response_get.headers)
    print('------ tělo -------')
    vystup = response_get.text[:100]
    print(f'{Fore.CYAN}{vystup}{Fore.RESET}')
    print('- Rozdíl hlaviček -')

    ddiff = DeepDiff(json1, json2, ignore_order=True)

    # Kontroly rozdílů
    # Zpracování 'dictionary_item_added'
    if 'dictionary_item_added' in ddiff:
        added_keys = [cojejinak.split('[')[1].strip(']') for cojejinak in ddiff['dictionary_item_added']]
        max_key_length_added = max(len(key) for key in added_keys) if added_keys else 0
        print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
        for klic in added_keys:
            print(f"  {Fore.YELLOW}{klic:<{max_key_length_added}}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET je navíc:{Fore.RESET}')
        print(f"-")

    # Zpracování 'dictionary_item_removed'
    if 'dictionary_item_removed' in ddiff:
        removed_keys = [cojejinak.split('[')[1].strip(']') for cojejinak in ddiff['dictionary_item_removed']]
        max_key_length_removed = max(len(key) for key in removed_keys) if removed_keys else 0
        print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
        for klic in removed_keys:
            print(f"  {Fore.YELLOW}{klic:<{max_key_length_removed}}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET chybí:{Fore.RESET}')
        print(f"-")

    # Zpracování 'values_changed'
    if 'values_changed' in ddiff:
        changed_keys = [cojejinak.split('[')[1].strip(']') for cojejinak in ddiff['values_changed']]
        max_key_length_changed = max(len(key) for key in changed_keys) if changed_keys else 0
        print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
        for cojejinak in ddiff['values_changed']:
            klic = cojejinak.split('[')[1].strip(']')
            old_val = ddiff['values_changed'][cojejinak]['old_value']
            new_val = ddiff['values_changed'][cojejinak]['new_value']
            print(f"  {Fore.YELLOW}{klic:<{max_key_length_changed}}{Fore.RESET}: {Fore.CYAN}{old_val}{Fore.RESET} -> {Fore.CYAN}{new_val}{Fore.RESET}")
    else:
        print(f'{Fore.RED}V GET je jinak:{Fore.RESET}')
        print(f"-")

except requests.exceptions.RequestException as e:
    print(f"{Fore.RED}Došlo k chybě při odesílání requestu: {e}{Fore.RESET}")