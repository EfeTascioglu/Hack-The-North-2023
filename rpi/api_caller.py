from threading import Thread
from queue import Queue, Empty

import requests

class APICaller(Thread):
    def __init__(self, url: str, reqs: Queue, resps: Queue):
        super().__init__()
        self.reqs = reqs
        self.resps = resps
        self.url = url
    
    def run(self):
        while True:
            req = self.reqs.get(True, None)
            endpoint, method, payload = req
            endpoint = self.url + endpoint
            if method == "POST":
                resp = requests.post(endpoint, json=payload).json()
                self.resps.put_nowait(resp)
            
