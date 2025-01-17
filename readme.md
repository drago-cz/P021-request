A Python script designed to send HTTP `HEAD` and `GET` requests to specified URLs, measure response times, and compare response headers. This tool is useful for monitoring website performance, validating server responses, and debugging HTTP interactions.

## Features

- **URL Validation**: Ensures that the provided URL has a valid scheme (`http` or `https`) and domain.
- **IP Address Handling**: Allows specifying an origin IP address or automatically resolves the IP via DNS.
- **Custom Headers**: Utilizes customizable HTTP headers to mimic specific client behaviors.
- **Response Measurement**: Measures and displays the response time for both `HEAD` and `GET` requests.
- **Header Comparison**: Compares headers from `HEAD` and `GET` responses, highlighting differences.
- **Color-Coded Output**: Uses colored text for better readability and easier identification of information.
- **Error Handling**: Gracefully handles connection errors, timeouts, and other request exceptions without interrupting the script.

## Requirements

- Python 3.6 or higher
- The following Python packages:
  - `requests`
  - `deepdiff`
  - `colorama`
  
You can install the required packages using `pip`:

```bash
pip install requests deepdiff colorama
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/drago-cz/P021-request.git
   cd url-response-measurement
   ```

2. **Install Dependencies**

   Ensure you have Python 3.6+ installed. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install them manually:*

   ```bash
   pip install requests deepdiff colorama
   ```

## Usage

Run the script using Python:

```bash
python main.py
```

### Steps:

1. **Enter URL**: When prompted, input the URL you want to verify. Ensure it starts with `http://` or `https://`. Type `exit` to terminate the script.
   
   ```
   Zadejte URL kterou prověříme (nebo 'exit' pro ukončení):
   ```

2. **Specify Origin IP (Optional)**: Enter the IP address where the domain should resolve (origin server). Leave blank to automatically resolve via DNS. Type `exit` to terminate.

   ```
   Zadej IP adresu, kde má doména být (origin server), anebo nech prázdné pro získání IP z DNS:
   ```

3. **View Results**: The script will send `HEAD` and `GET` requests to the provided URL, display response codes, response times, headers, and differences between `HEAD` and `GET` responses.

4. **Repeat**: After completing the requests, you can enter another URL or type `exit` to quit.

## Example

```bash
$ python script.py
Zadejte URL kterou prověříme (nebo 'exit' pro ukončení): https://www.example.com
Zadej IP adresu, kde má doména být (origin server), anebo nech prázdné pro získání IP z DNS:
IP adresa pro www.example.com (získáno z DNS): 93.184.216.34

Posílám request na https://93.184.216.34 typu HEAD
Odpověď vrátila kód 200 trvala 0.123 sekund.
---- hlavička  ----
Content-Type : text/html; charset=UTF-8
Content-Length : 1256
...

Posílám request na https://93.184.216.34 typu GET
Odpověď vrátila kód 200 trvala 0.456 sekund.
---- hlavička  ----
Content-Type : text/html; charset=UTF-8
Content-Length : 1256
...
- Rozdíl hlaviček -
V GET je navíc:
  -
V GET chybí:
  -
V GET je jinak:
  -
```

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to [ChatGPT-4o](https://chatgpt.com/) and [ChatGPT o1-mini](https://chatgpt.com/) for their assistance in developing this script.

# Disclaimer

Use this script responsibly. Ensure you have permission to send requests to the target URLs to avoid violating any terms of service or legal regulations.
