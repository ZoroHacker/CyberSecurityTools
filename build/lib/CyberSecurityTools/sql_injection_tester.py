import requests

class SQLInjectionTester:
    def __init__(self):
        pass

    def test(self, url, param):
        payloads = ["' OR '1'='1", "' OR 'a'='a", "' OR ''='"]
        vulnerable = False
        for payload in payloads:
            full_url = f"{url}?{param}={payload}"
            try:
                response = requests.get(full_url)
                print(f"Testing URL: {full_url} - Status Code: {response.status_code}")
                if any(error in response.text.lower() for error in ["mysql", "syntax error", "sql"]):
                    print(f"Potential SQL injection vulnerability at {full_url}")
                    vulnerable = True
                    break
            except requests.RequestException as e:
                print(f"Error accessing {full_url}: {e}")
        return vulnerable
