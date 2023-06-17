import json

import requests

import paths
from dtos import DataDTO, BulkDataDTO, update_decoder


class HttpImpl:
    def __init__(self, hostname):
        self.hostname = hostname

        self.headers = {"content-type": "application/json", "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtZG1hLWJhY2tlbmQiLCJzdWIiOiJINHI0bGREM3JINGNrM3IiLCJleHAiOjE2ODcwNzI4MTcsIm5iZiI6MTY4Njk4NjQxNywiaWF0IjoxNjg2OTg2NDE3LCJyb2xlIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJtZXNoX25vZGVfY3JlYXRlIiwibWVzaF9ub2RlX3JlYWQiLCJtZXNoX25vZGVfdXBkYXRlIiwibWVzaF9ub2RlX2RlbGV0ZSIsIm1lc2hfbm9kZV91cGRhdGVfY3JlYXRlIiwibWVzaF9ub2RlX3VwZGF0ZV9yZWFkIiwibWVzaF9ub2RlX3VwZGF0ZV9kZWxldGUiLCJkYXRhX2NyZWF0ZSIsImRhdGFfcmVhZCIsImRhdGFfZGVsZXRlIiwidXNlcl9hY2NvdW50X2NyZWF0ZSIsInVzZXJfYWNjb3VudF9yZWFkIiwidXNlcl9hY2NvdW50X3VwZGF0ZSIsInVzZXJfYWNjb3VudF9kZWxldGUiLCJzZXJ2aWNlX2FjY291bnRfY3JlYXRlIiwic2VydmljZV9hY2NvdW50X3JlYWQiLCJzZXJ2aWNlX2FjY291bnRfdXBkYXRlIiwic2VydmljZV9hY2NvdW50X2RlbGV0ZSIsInJvbGVfY3JlYXRlIiwicm9sZV9yZWFkIiwicm9sZV91cGRhdGUiLCJyb2xlX2RlbGV0ZSJdfQ.LPGiBzZgZRdOiBRJXy7rayZzz0MNAXw66wX2PISXlng"}

    def post_node_data(self, uuid, data_dto: DataDTO):
        path = f'{paths.meshNodesBaseUrl}{uuid}{paths.meshNodesDataSuffix}'
        url = f'{self.hostname}{path}'
        response = requests.post(url, data_dto.to_json(), headers=self.headers)
        handle_response(response)

    # use only for sending system info data
    def post_node_data_bulk(self, uuid, data_dto_bulk: BulkDataDTO):
        path = f'{paths.meshNodesBaseUrl}{uuid}{paths.meshNodesDataListSuffix}'
        url = f'{self.hostname}{path}'
        response = requests.post(url, data_dto_bulk.to_json(), headers=self.headers)
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
