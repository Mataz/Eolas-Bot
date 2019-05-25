import json
import requests

class HTTPRequests(object):
    def __init__(self):
        self.debug = True
        self.verify = False

    def makeRequest(requestURL, methods: str):
        source = f"requests.{methods}(url=str({requestURL}))"
        reponse = source.json()
        response = json.dumps(response, indent=3, sort_Keys=True)
        return response

    def 