import requests

class CSRFTester:
    def __init__(self):
        pass

    def test(self, form_url, form_data):
        # Assume form_data is a dictionary of form fields
        print(f"Testing for CSRF at {form_url}")
        try:
            response = requests.post(form_url, data=form_data)
            if response.status_code == 200:
                print(f"Form submission succeeded without CSRF token: {form_url}")
                return True
            else:
                print(f"Form submission failed or has token protection: {form_url}")
        except requests.RequestException as e:
            print(f"Error submitting form: {e}")
        return False
