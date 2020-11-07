from urllib.parse import urljoin
from flask import jsonify
#from urllib import urlencode
import requests

class DataLayer():
    auth = requests.auth.HTTPDigestAuth("admin","admin")
    host = 'http://localhost:8055/v1/'
    endpoints = ['documents?uri=', 'search?q=']

    def getJsonDoc(self, uri):
        link = "{}{}{}".format(self.host, self.endpoints[0], uri)
        resp = requests.get(link, auth = self.auth)
        return resp.json()

    def getBinaryDoc(self, uri):
        link = "{}{}{}".format(self.host, self.endpoints[0], uri)
        resp = requests.get(link, auth = self.auth)
        return resp

    def searchJsonDoc(self, query):
        link = "{}{}{}&format=json".format(self.host, self.endpoints[1], query)
        #print("link: ", link)
        resp = requests.get(link, auth = self.auth)
        print(resp)
        return resp.json()['results']



#ttp://localhost:8055/v1/documents?uri=/image/MalikBeasley.png
