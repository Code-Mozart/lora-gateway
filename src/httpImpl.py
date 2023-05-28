import requests
import json
import paths
import dtos


class HttpImpl:
    def __init__(self, hostname):
        self.hostname = hostname

        self.headers = {"content-type": "application/json"}

    def post_node_data(self, uuid, data_dto: dtos.DataDTO):
        path = f'{paths.meshNodesBaseUrl}{uuid}{paths.meshNodesDataSuffix}'
        url = f'{self.hostname}{path}'
        response = requests.post(url, data_dto.to_json(), headers=self.headers)
        handle_response(response)

    def get_update(self):
        path = f'{paths.updateBaseUrl}'
        url = f'{self.hostname}{path}'
        response = requests.get(url)

        try:
            return handle_response(response, dtos.update_decoder)
        except Exception as e:
            raise Exception(str(e))


def handle_response(response, decoder=None):

    content = json.loads(response.content.decode('utf-8'))

    match response.status_code:
        case 200:
            print(f'Successful {response.request.method} request to {response.request.url}: \n{content}')
            return decode_content(content, decoder)
        case 201:
            print(f'Created at {response.request.url}: \n{content}')
            return decode_content(content, decoder)
        case 401:
            raise Exception(f'Unauthorized {response.request.url}: \n{content}')
        case 403:
            raise Exception(f'Forbidden: {response.request.url}: \n{content}')
        case 404:
            raise Exception(f'Unknown URL {response.request.url}: \n{content}')
        case _:
            raise Exception(f'Bad Request {response.request.url}: \n{content}')


def decode_content(content, decoder=None):

    if decoder is not None:
        return decoder(content)

    return None
