# middleware.py

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class DisableSSLVerificationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Disable SSL certificate verification for outgoing requests
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        return self.get_response(request)
