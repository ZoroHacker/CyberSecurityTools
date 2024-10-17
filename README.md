# CyberSecurityTool

**CyberSecurityTool** is a comprehensive Python package designed for performing essential cybersecurity scans. It includes tools for subdomain enumeration, broken link checking, SQL injection testing, XSS detection, CSRF testing, and network vulnerability scanning. Built with ease of use and efficiency in mind, CyberSecurityTool empowers developers and security professionals to enhance their web application's security and identify vulnerabilities with minimal effort.

## Features

- **Subdomain Enumeration**: Identify valid subdomains for a given domain using a wordlist.
- **Broken Link Checker**: Scan webpages for broken or unreachable links.
- **SQL Injection Tester**: Detect potential SQL injection vulnerabilities.
- **XSS Tester**: Identify cross-site scripting (XSS) vulnerabilities in web applications.
- **CSRF Tester**: Test for Cross-Site Request Forgery (CSRF) vulnerabilities.
- **Network Vulnerability Scanner**: Scan for open network ports on a given host.

## Installation

You can install CyberSecurityTool using `pip`: 

```bash
pip install CyberSecurityTool

```

## How To Use

**Subdomain Enumeration**

```python
from CyberSecurityTools import SubdomainEnumerator

# Subdomain Enumeration
subdomain_enum = SubdomainEnumerator(base_domain="example.com")
subdomains = subdomain_enum.enumerate(wordlist_path="wordlist.txt")
print(subdomains)
```

**Broken Link Checker**

```python
from CyberSecurityTools import BrokenLinkChecker

# Broken Link Checker
broken_link_checker = BrokenLinkChecker()
broken_links = broken_link_checker.check(url="http://testphp.vulnweb.com")
print(f"Broken Links Found: {broken_links}")
```

**SQL Injection Tester**

```python
from CyberSecurityTools import SQLInjectionTester

# SQL Injection Testing
sql_tester = SQLInjectionTester()
vulnerable = sql_tester.test(url="http://testphp.vulnweb.com/listproducts.php", param="cat")
print(f"SQL Injection Vulnerability Found: {vulnerable}")
```

**XSS Tester**

```python
from CyberSecurityTools import XSSTester

# XSS Testing
xss_tester = XSSTester()
vulnerable = xss_tester.test(url="http://testphp.vulnweb.com/comment.php", param="name")
print(f"XSS Vulnerability Found: {vulnerable}")
```

**CSRF Tester**

```python
from CyberSecurityTools import CSRFTester

# CSRF Testing
csrf_tester = CSRFTester()
vulnerable = csrf_tester.test(form_url="http://testphp.vulnweb.com/login.php", form_data={"username": "test", "password": "pass"})
print(f"CSRF Vulnerability Found: {vulnerable}")
```

**Network Vulnerability Scanner**

```python
from CyberSecurityTools import NetworkVulnerabilityScanner

# Network Vulnerability Scanning
network_scanner = NetworkVulnerabilityScanner(target="192.168.1.1")
open_ports = network_scanner.scan()
print(f"Open Ports: {open_ports}")
```
