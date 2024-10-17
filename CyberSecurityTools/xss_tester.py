import requests

class XSSTester:
    def __init__(self):
        pass

    def test(self, url, param):
        payloads = ['<script>alert("XSS")</script>', '"><script>alert(1)</script>']
        vulnerable = False
        for payload in payloads:
            full_url = f"{url}?{param}={payload}"
            try:
                response = requests.get(full_url)
                print(f"Testing URL: {full_url} - Status Code: {response.status_code}")
                if payload in response.text:
                    print(f"Potential XSS vulnerability at {full_url}")
                    vulnerable = True
                    break
            except requests.RequestException as e:
                print(f"Error accessing {full_url}: {e}")
        return vulnerable
