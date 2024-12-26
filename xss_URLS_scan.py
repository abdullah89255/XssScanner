import requests
from bs4 import BeautifulSoup
import sys

def load_payloads(file_path):
    """Load XSS payloads from a file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Payload file not found: {file_path}")
        sys.exit(1)

def fetch_url_content(url):
    """Fetch content of the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching URL {url}: {e}")
        return None

def get_forms_from_html(html):
    """Extract forms from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('form')

def build_action_url(base_url, action):
    """Construct the full action URL."""
    if action is None or action.strip() == "":
        return base_url
    if action.startswith("http"):
        return action
    return requests.compat.urljoin(base_url, action)

def scan_xss(url, payloads):
    """Scan the URL for XSS vulnerabilities."""
    results = []
    html_content = fetch_url_content(url)
    if html_content is None:
        return results

    forms = get_forms_from_html(html_content)
    if not forms:
        print("[+] No forms found on the page.")
        return results

    for form in forms:
        action = form.get('action')
        method = form.get('method', 'GET').upper()
        action_url = build_action_url(url, action)

        print(f"[+] Testing form with action: {action_url} and method: {method}")

        inputs = form.find_all('input')
        for payload in payloads:
            data = {}
            for input_field in inputs:
                if input_field.get('type', '').lower() in ['text', 'search']:
                    name = input_field.get('name')
                    if name:
                        data[name] = payload

            try:
                if method == 'GET':
                    response = requests.get(action_url, params=data, timeout=10)
                elif method == 'POST':
                    response = requests.post(action_url, data=data, timeout=10)
                else:
                    print(f"[!] Unsupported form method: {method}")
                    continue

                if payload in response.text:
                    print(f"[!!!] Vulnerable to XSS with payload: {payload}")
                    results.append((action_url, payload))
            except requests.exceptions.RequestException as e:
                print(f"[!] Error submitting form to {action_url}: {e}")

    return results

def scan_urls_from_file(file_path, payloads):
    """Scan URLs from a file."""
    results = []
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
            for url in urls:
                print(f"[+] Scanning URL: {url}")
                results.extend(scan_xss(url, payloads))
    except FileNotFoundError:
        print(f"[!] URL file not found: {file_path}")
        sys.exit(1)
    return results

def main():
    """Main entry point of the script."""
    if len(sys.argv) != 3:
        print("Usage: python3 xss_URLS_scan.py <urls_file> <payloads_file>")
        sys.exit(1)

    urls_file = sys.argv[1]
    payloads_file = sys.argv[2]

    payloads = load_payloads(payloads_file)
    results = scan_urls_from_file(urls_file, payloads)

    print("\n[+] Scan complete!")
    if results:
        print("[+] Vulnerabilities found:")
        for url, payload in results:
            print(f"URL: {url}, Payload: {payload}")
    else:
        print("[+] No vulnerabilities found.")

if __name__ == "__main__":
    main()
