from base64 import b64encode
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
        #print(type(resp.content)) <class 'bytes'>
        image = b64encode(resp.content).decode('utf')
        return image

    def searchJsonDoc(self, query):
        link = "{}{}{}&format=json&pageLength=18".format(self.host, self.endpoints[1], query)
        resp = requests.get(link, auth = self.auth)
        return resp.json()['results']


    def getJsonDocs(self, uris):
        result=[]
        for uri in uris:
            link = "{}{}{}".format(self.host, self.endpoints[0], uri)
            resp = requests.get(link, auth = self.auth) 
            result.append(resp.json())
        return result
   


