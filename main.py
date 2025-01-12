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

init(convert=True)

#url = 'https://solana.bool.cz'
#url = 'http://404m.com'

# Zeptej se na IP adresu
url = input("Zadejte URL kterou prověříme): ").strip()


#headers = {'User-Agent': 'WEDOS OnLine monitoring; https://www.wedos.online/'}
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#headers = {'User-Agent': 'Test B'}
headers = {'User-Agent': 'Inteligent Verification Autonomous Network/CyberOS 5.0 (SynthOS NT 10.0; Synth64; x64) CyberCode/537.36 (HyperHTML, like Quantum) Quantum/537.36'}

#headers['Accept-Language'] = 'cs-CZ,cs;q=0.9,en-US;q=0.8,en;q=0.7'
headers['Accept-Language'] = 'en-US;q=0.8,en;q=0.7'

print(f"Useragent: {Fore.GREEN}{headers}{Fore.RESET}")

print(f"Posílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}HEAD{Fore.RESET}")
start = time.time()

response = requests.head(url, headers=headers, stream=True, allow_redirects=False)
json1       = response.headers
status_1    = response.status_code
#print (response.raw._connection.sock.getsockname())
end = time.time()

print(f"Odpověď z vrátila kód {Fore.CYAN}{status_1}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
print('---- hlavička  ----')
#print(f'{Fore.CYAN}{response.headers}{Fore.RESET}')
for key, value in response.headers.items():
    print(f'  {Fore.YELLOW}{key}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}')
print('------ tělo -------')
print(f'{Fore.CYAN}{response.text}{Fore.RESET}')

# ------------

print(f"Posílám request na {Fore.YELLOW}{url}{Fore.RESET} typu {Fore.GREEN}GET{Fore.RESET}")
start = time.time()

response = requests.get(url, headers=headers, allow_redirects=False)
json2 = response.headers
status_2 = response.status_code
end = time.time()

print(f"Odpověď z vrátila kód {Fore.CYAN}{status_2}{Fore.RESET} trvala {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} sekund.")
print('---- hlavička  ----')
#print(f'{Fore.CYAN}{response.headers}{Fore.RESET}')
for key, value in response.headers.items():
    print(f'  {Fore.YELLOW}{key}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}')
print('------ tělo -------')
vystup = response.text
vystup = vystup[:100]
print(f'{Fore.CYAN}{vystup}{Fore.RESET}')
print('- Rozdíl hlaviček -')

ddiff = DeepDiff(json1, json2, ignore_order=True)

# Tady začínají vaše kontroly
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