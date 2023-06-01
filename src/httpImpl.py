import json

import requests

import paths
from dtos import DataDTO, update_decoder


class HttpImpl:
    def __init__(self, hostname):
        self.hostname = hostname

        self.headers = {"content-type": "application/json"}
        # TODO: JWT Token for header

    def post_node_data(self, uuid, data_dto: DataDTO):
        path = f'{paths.meshNodesBaseUrl}{uuid}{paths.meshNodesDataSuffix}'
        url = f'{self.hostname}{path}'
        response = requests.post(url, data_dto.to_json(), headers=self.headers)
        handle_response(response)

    def get_update(self):
        path = f'{paths.updateBaseUrl}'
        url = f'{self.hostname}{path}'
        response = requests.get(url)

        try:
            return handle_response(response, update_decoder)
        except Exception as e:
            raise Exception(str(e))


def handle_response(response, decoder=None):
    content = json.loads(response.content.decode('utf-8'))
    handled = False
    if response.status_code == 200:
        print(f'Successful {response.request.method} request to {response.request.url}: \n{content}')
        handled = True
        return decode_content(content, decoder)
    if response.status_code == 201:
        print(f'Created at {response.request.url}: \n{content}')
        handled = True
        return decode_content(content, decoder)
    if response.status_code == 401:
        handled = True
        raise Exception(f'Unauthorized {response.request.url}: \n{content}')
    if response.status_code == 403:
        handled = True
        raise Exception(f'Forbidden: {response.request.url}: \n{content}')
    if response.status_code == 404:
        handled = True
        raise Exception(f'Unknown URL {response.request.url}: \n{content}')
    if not handled:
        raise Exception(f'Bad Request {response.request.url}: \n{content}')


def decode_content(content, decoder=None):

    if decoder is not None:
        return decoder(content)

    return None
