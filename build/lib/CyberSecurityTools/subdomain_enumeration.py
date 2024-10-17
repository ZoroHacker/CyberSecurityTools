import requests

class SubdomainEnumerator:
    def __init__(self, base_domain):
        self.base_domain = base_domain

    def enumerate(self, wordlist_path):
        found_subdomains = []
        try:
            with open(wordlist_path, 'r') as file:
                subdomains = file.read().splitlines()

            for subdomain in subdomains:
                url = f"http://{subdomain}.{self.base_domain}"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(f"Found: {url}")
                        found_subdomains.append(url)
                except requests.ConnectionError:
                    print(f"Failed to connect to: {url}")
        except FileNotFoundError:
            print(f"Wordlist file not found: {wordlist_path}")
        return found_subdomains
