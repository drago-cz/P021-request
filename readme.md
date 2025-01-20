# HTTP Request Debugging Tool (`main.py`)

This Python script combines functionality from two original scripts I developed as a proof of concept and improves upon them with enhancements and detailed inline documentation (special thanks to ChatGPT 4o for assistance). The script is a simple tool for comparing HTTP `HEAD` and `GET` requests, measuring response times, and optionally sending requests directly to the origin server using its IP address.

## Repository

[GitHub Repository: drago-cz/P021-request](https://github.com/drago-cz/P021-request)

## Use case and origin

The current script is a combination of two scripts I made for two different user cases.

### 1. Debugging Slow Response Times for `HEAD` Requests
A customer reported that the [WEDOS OnLine monitoring tool](https://www.wedos.online/) showed their website as slow, despite it loading quickly in practice. Upon reviewing the access logs, I discovered that `HEAD` requests were indeed slower. To confirm this behavior, I developed the initial script to compare the response times of `HEAD` and `GET` requests.

This tool revealed that the customer's CMS did not return cached responses for `HEAD` requests. Based on these findings, WEDOS OnLine was updated to allow users to choose between `HEAD` and `GET` for availability checks.

### 2. Sending Requests Directly to the Origin Server
The second script was an evolution of the first, adding the capability to send requests directly to the origin web server using its IP address. This functionality is particularly useful when:
- Planning to migrate a website to a new hosting provider.
- Investigating issues behind a reverse proxy.

Both scripts were eventually merged into this single, improved version (`main.py`).

## Features

- **URL Validation**: Ensures the provided URL is valid before sending requests.
- **HEAD vs. GET Comparison**: Measures and compares response times and headers for both request types.
- **Direct Origin Requests**: Supports sending requests to the origin server using its IP address instead of the domain name.
- **Detailed Header Analysis**:
  - Detects and reports differences between `HEAD` and `GET` responses.
  - Highlights added, missing, or changed headers.
- **DNS Resolution**: Automatically resolves the IP address of a domain if no origin IP is provided.
- **Error Handling**: Robust exception handling for connection errors, timeouts, and other issues.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/drago-cz/P021-request.git
   ```
2. Navigate to the project directory:
   ```bash
   cd P021-request
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using Python:

```bash
python main.py
```

Follow the prompts to:
1. Input a URL to test (Including HTTP or HTTPS).
2. Optionally specify the origin server's IP address.

The script will display:
- Response times for `HEAD` and `GET` requests.
- Header differences between the two request types.
- The first 100 characters of the response body (for `GET` requests).
- Detailed error messages for failed requests.

## Requirements

- Python 3.7 or higher
- Required libraries (install via `pip`):
  - `requests`
  - `colorama`
  - `deepdiff`

## Notes

- SSL certificate warnings are disabled for testing purposes.
- The script's colored terminal output is compatible with Windows, thanks to the `colorama` library.

## Acknowledgments

Special thanks to **ChatGPT 4o** for assistance with documentation and code refinement.
