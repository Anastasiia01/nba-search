from urllib.parse import urljoin
from urllib import urlencode
import requests

class DataLayer():
    self.auth = requests.auth.HTTPDigestAuth("admin","admin")
    self.host = 'http://localhost:8070/v1/'
    self.endpoints = ['documents', 'search']
