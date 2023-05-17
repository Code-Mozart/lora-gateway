import requests
from http import HTTPStatus


class HttpImpl:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_data(self):
        print("send data")
        # handle response

    def pull_update(self):
        print("pull update")

