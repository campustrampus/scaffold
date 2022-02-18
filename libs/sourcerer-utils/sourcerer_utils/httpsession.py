from urllib3.util import Retry
import requests
from requests.adapters import HTTPAdapter


class HTTPSession:
    """
    A class that contains a base url and request session
            Parameters:
                base_url (str): A base url for an api
                token (str): A basic auth token base64 encoded
                retries (int) = number of retries to perform
                                default = 3
    """
    def __init__(self, base_url: str, token: str, retries: int = 3):
        self.base_url = base_url
        self.session = requests.Session()

        retry = Retry(total=retries,
                      read=retries,
                      connect=retries,
                      backoff_factor=0.3,
                      allowed_methods=None,
                      status_forcelist=(500, 502, 503, 504))

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

        headers = {
            "Authorization": f'Basic {token}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session.headers.update(headers)
