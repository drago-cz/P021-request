# This script is designed to send HTTP requests (HEAD and GET) to a specified URL,
# measure response times, and analyze differences in headers between the two request types.
# It validates input URLs and IP addresses, resolves DNS when necessary, and provides
# detailed feedback on HTTP responses, including status codes, headers, and response body excerpts.
# The script includes error handling for connection issues and timeout scenarios, ensuring robustness during execution.

import requests
import time
from deepdiff import DeepDiff
from colorama import init, Fore
from urllib.parse import urlparse
import socket
import ipaddress
import urllib3

# Disables warnings related to insecure HTTPS requests (e.g., when SSL certificate verification is turned off).
# This is done to prevent cluttering the output with warnings, especially during testing.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initializes the Colorama library for cross-platform support of colored terminal text.
# The `convert=True` argument ensures compatibility with Windows terminals by converting ANSI escape sequences.
init(convert=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US;q=0.8,en;q=0.7'
}

# Validates whether a given string is a properly formatted URL.
# It ensures the URL:
# 1. Has a valid scheme ('http' or 'https').
# 2. Contains a network location (domain or IP address).
# Returns True if the URL is valid, otherwise False.
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and bool(parsed.netloc)
    except Exception:
        return False

# Continuously prompts the user to input a valid URL until a valid one is provided.
# Returns the first valid URL inputted by the user.
def get_valid_url():
    while True:
        url = input("Enter the URL to verify (or type 'exit' to quit): ").strip()
        # Accepts 'exit' (case-insensitive) as input to terminate the script gracefully.
        if url.lower() == 'exit':
            print("Terminating the script.")
            exit(0)
        # Uses `is_valid_url()` to check if the URL meets the required format.
        if is_valid_url(url):
            return url
        # Displays a red error message for invalid URLs and asks the user to try again.
        else:
            print(f"{Fore.RED}Invalid URL. Please try again.{Fore.RESET}")

# Continuously prompts the user to input an IP address or leave it blank.
# Returns the valid IP address entered by the user or False if left blank.
def get_and_validate_ip():
    while True:
        ip = input("Enter the IP address of the domain (origin server), or leave blank to resolve IP via DNS: ").strip()
        # If the input is blank, it returns False to indicate that the IP address should be resolved via DNS.
        if ip == '':
            return False
        # If the user inputs 'exit' (case-insensitive), the script terminates gracefully.
        if ip.lower() == 'exit':
            print("Terminating the script.")
            exit(0)

        try:
            # Validates the input using `ipaddress.ip_address()` to ensure it is a valid IP address.
            ipaddress.ip_address(ip)
            # Returns the valid IP address entered by the user .
            return ip
        except ValueError:
            # Displays a red error message for invalid IP addresses and asks the user to try again.
            print(f"{Fore.RED}Invalid IP address. Please try again.{Fore.RESET}")


# Prints HTTP headers in a formatted and aligned manner for better readability.
# Accepts a dictionary of headers (`headers_dict`) as input.
def print_headers(headers_dict):
    # If the headers dictionary is empty, displays a yellow message indicating no headers are available.
    if not headers_dict:
        print(f"{Fore.YELLOW}No headers to display.{Fore.RESET}")
        return

    # Calculates the maximum length of the header keys to align the output neatly.
    max_key_length = max(len(key) for key in headers_dict.keys())

    for key, value in headers_dict.items():
        print(f"  {Fore.YELLOW}{key:<{max_key_length}}{Fore.RESET}: {Fore.CYAN}{value}{Fore.RESET}")


while True:
    url = get_valid_url()
    parsed_url = urlparse(url)
    host = parsed_url.hostname
    origin_ip = get_and_validate_ip()

    # Resolves the IP address for the given host if the `origin_ip` is not provided (False).
    if origin_ip == False:
        # Attempts to resolve the host's IP address using `socket.gethostbyname()`.
        try:
            ip_address = socket.gethostbyname(host)
            print(f"{Fore.GREEN}IP address for {host} (resolved via DNS): {ip_address}{Fore.RESET}")
        # On failure (e.g., DNS resolution error), displays a red error message and skips further requests for the current URL.
        except socket.gaierror:
            print(f"{Fore.RED}Error: Unable to resolve IP address for the host '{host}'.{Fore.RESET}")
            print("\n--- No point in sending further requests ---\n")
            continue  # Přeskočí GET request a pokračuje s další URL
    # If `origin_ip` is provided, it is directly assigned as the target IP address and printed in green.
    else:
        ip_address = origin_ip
        print(f"{Fore.GREEN}Origin IP address provided: {ip_address}{Fore.RESET}")

    # Sends a HEAD request to the specified URL and prepares headers and URL for cases with a custom origin IP.
    try:
        # Records the start time for measuring the response duration.
        start = time.time()

        # If a custom origin IP is provided
        if origin_ip: 
            # Adds the original host to the headers for proper request routing.
            headers['Host'] = host

            print(f"Final headers being sent:{Fore.GREEN}{headers}{Fore.RESET}")

            parsed_url = urlparse(url)      # Parse the original URL to extract components like protocol, path, and query string     
            protocol = parsed_url.scheme    # The protocol (http or https).
            path = parsed_url.path          # The path (e.g., /folder/file).
            query = parsed_url.query        # Query parameters (e.g., param1=value1&param2=value2).

             # Construct a new URL using the resolved or provided IP address.
            new_url = f"{protocol}://{ip_address}{path}"

            # Append query parameters if they exist.
            if query:  
                new_url += f"?{query}"

            # Display both the original and modified URLs for debugging.
            print("Original URL:", url)
            print("Modified URL with IP address:", new_url)

            url = new_url

        print(f"\nSending request to {Fore.YELLOW}{url}{Fore.RESET} of type {Fore.GREEN}HEAD{Fore.RESET}")

        # Sends a HEAD request to the target URL and processes the response.
        response_head = requests.head(
            url, 
            headers=headers, 
            allow_redirects=False,  # Prevents automatic redirection to preserve original request behavior.
            timeout=10,             # Sets a timeout of 10 seconds for the request.
            verify=False            # Disables SSL certificate verification for testing purposes.
        )

        # Extracts the headers and status code from the response.
        json1 = response_head.headers           # Extracts the headers from the response.
        status_1 = response_head.status_code    # Extracts the status code from the response.
        end = time.time()                       # Records the end time to calculate the total response duration.

        # Displays the HTTP status code and the time taken for the response.
        print(f"The response returned status code {Fore.CYAN}{status_1}{Fore.RESET} and took {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} seconds.")
        
        # Prints the headers from the response.
        print('---- Headers ----')
        print_headers(response_head.headers)
        
        # Checks if there is a response body (which is unusual for HEAD requests) and displays it if present.
        print('------ Body -------')
        if response_head.text:
            print(f'{Fore.CYAN}{response_head.text}{Fore.RESET}')
        else:
            print(f"{Fore.YELLOW}The response does not contain a body, as expected for a HEAD request.{Fore.RESET}")

    # Handles exceptions that may occur during the HEAD request.
    # Handles connection errors, such as the inability to reach the target server.
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Connection error. Unable to connect to {host} ({ip_address}). The target server is not responding.{Fore.RESET}")
    # Handles timeout errors when the server takes too long to respond.
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Connection timed out while trying to reach {host} ({ip_address}).{Fore.RESET}")
    # Catches any other request-related exceptions and displays the error message.
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}An error occurred while sending the HEAD request: {e}{Fore.RESET}")

    # Sends a GET request to the target URL, processes the response, and compares headers with a previous HEAD request.
    try:
        # Print the GET request initiation with the target URL.
        print(f"\nSending request to {Fore.YELLOW}{url}{Fore.RESET} of type {Fore.GREEN}GET{Fore.RESET}")
        start = time.time()

        # Sends the GET request with specified headers and settings.
        response_get = requests.get(
            url, 
            headers=headers, 
            allow_redirects=False,  # Disables automatic redirection.
            timeout=10,             # Sets a timeout of 10 seconds.
            verify=False            # Disables SSL verification for testing purposes.
        )
        json2 = response_get.headers         # Extracts response headers.
        status_2 = response_get.status_code  # Extracts the status code.
        end = time.time()                    # Records the end time for response duration.

        # Print the response status code and the duration of the GET request.
        print(f"The response returned status code {Fore.CYAN}{status_2}{Fore.RESET} and took {Fore.YELLOW}{round((end - start),3)}{Fore.RESET} seconds.")
        
        # Prints the response headers.
        print('---- Headers ----')
        print_headers(response_get.headers)
        
        # Displays the first 100 characters of the response body for quick inspection.
        print('------ Body -------')
        vystup = response_get.text[:100]
        print(f'{Fore.CYAN}{vystup}{Fore.RESET}')

        # Compares the HEAD and GET headers using DeepDiff.
        print('- Header Differences -')
        ddiff = DeepDiff(json1, json2, ignore_order=True)

        # Handles headers added in the GET response - 'dictionary_item_added'
        if 'dictionary_item_added' in ddiff:
            added_keys = [key.split('[')[1].strip(']') for key in ddiff['dictionary_item_added']]
            max_key_length_added = max(len(key) for key in added_keys) if added_keys else 0
            print(f'{Fore.RED}Additional headers in GET:{Fore.RESET}')
            for klic in added_keys:
                print(f"  {Fore.YELLOW}{klic:<{max_key_length_added}}{Fore.RESET}")
        else:
            print(f'{Fore.RED}Additional headers in GET:{Fore.RESET}')
            print(f"-")

        # Handles headers removed in the GET response - 'dictionary_item_removed'
        if 'dictionary_item_removed' in ddiff:
            removed_keys = [key.split('[')[1].strip(']') for key in ddiff['dictionary_item_removed']]
            max_key_length_removed = max(len(key) for key in removed_keys) if removed_keys else 0
            print(f'{Fore.RED}Missing headers in GET:{Fore.RESET}')
            for klic in removed_keys:
                print(f"  {Fore.YELLOW}{klic:<{max_key_length_removed}}{Fore.RESET}")
        else:
            print(f'{Fore.RED}Missing headers in GET:{Fore.RESET}')
            print(f"-")

        # Handles headers with changed values in the GET response - 'values_changed'
        if 'values_changed' in ddiff:
            print(f'{Fore.RED}Headers differ in GET:{Fore.RESET}')
            for key, change in ddiff['values_changed'].items():
                klic = key.split('[')[1].strip(']')
                old_val = change['old_value']
                new_val = change['new_value']
                print(f"  {Fore.YELLOW}{klic}{Fore.RESET}: {Fore.CYAN}{old_val}{Fore.RESET} -> {Fore.CYAN}{new_val}{Fore.RESET}")
        else:
            print(f'{Fore.RED}Headers differ in GET:{Fore.RESET}')
            print(f"-")

    # Print an error for connection issues during the GET request.
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Connection error. Unable to connect to {host} ({ip_address}). The target server is not responding.{Fore.RESET}")
    # Handles timeout errors when the server takes too long to respond.
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Connection timed out while trying to reach {host} ({ip_address}).{Fore.RESET}")
    # Catches any other request-related exceptions and displays the error message.
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}An error occurred while sending the HEAD request: {e}{Fore.RESET}")

    # Print the transition to the next URL after processing the current one.
    print("\n--- Next URL ---\n")