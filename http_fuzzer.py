import requests
import sys
import csv

# Default timeout is 3 seconds
timeout_val = 3

# Check if user passed --timeout argument
if '--timeout' in sys.argv:
    try:
        timeout_val = int(sys.argv[sys.argv.index('--timeout') + 1])
    except (IndexError, ValueError):
        print("Error: --timeout requires a number. Using default 3s.")

# List of subdomains to test
subdomains = [
    'www.tesla.com',
    'dev.tesla.com',
    'api.tesla.com',
    'ir.tesla.com'
]

print(f"Starting fuzzer with timeout: {timeout_val} seconds...\n")

with open('subdomain_results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Subdomain', 'Protocol', 'Status Code', 'Response Length'])

    for sub in subdomains:
        for protocol in ['https://', 'http://']:
            url = f"{protocol}{sub}"

            try:
                # Added timeout argument here
                response = requests.get(url, timeout=timeout_val)
                status = response.status_code
                length = len(response.text)

                print(f"[+] {url} -> Status: {status} | Length: {length}")
                writer.writerow([sub, protocol, status, length])

            except requests.exceptions.Timeout:
                print(f"[-] {url} -> TIMEOUT after {timeout_val}s")
                writer.writerow([sub, protocol, "TIMEOUT", "0"])
            except requests.exceptions.RequestException as e:
                print(f"[-] {url} -> ERROR: {e}")
                writer.writerow([sub, protocol, "ERROR", "0"])

print("\nDone! Results saved to subdomain_results.csv")