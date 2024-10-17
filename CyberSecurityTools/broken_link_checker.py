import requests
from bs4 import BeautifulSoup

class BrokenLinkChecker:
    def __init__(self):
        pass

    def check(self, url):
        broken_links = []
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            print(f"Found {len(links)} links on {url}")  # Debugging info

            for link in links:
                link_url = link['href']
                try:
                    r = requests.head(link_url, allow_redirects=True)
                    if r.status_code >= 400:
                        print(f"Broken link: {link_url} with status {r.status_code}")
                        broken_links.append(link_url)
                except requests.RequestException as e:
                    print(f"Error checking {link_url}: {e}")
                    broken_links.append(link_url)

        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        
        return broken_links
