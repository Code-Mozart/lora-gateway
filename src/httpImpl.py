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
        self.handle_response(response)

    def get_update(self):
        path = f'{paths.updateBaseUrl}'
        url = f'{self.hostname}{path}'
        response = requests.get(url)
        if not self.handle_response(response):
            print("Failed to fetch update")
            return

        return dtos.update_decoder(json.loads(response.content.decode('utf-8')))

    def handle_response(self, response):

        content = response.content.decode('utf-8')

        match response.status_code:
            case 200:
                print(f'Successful {response.request.method} request to {response.request.url}: \n{content}')
                return True
            case 201:
                print(f'Created at {response.request.url}: \n{content}')
                return True
            case 401:
                print(f'Unauthorized {response.request.url}: \n{content}')
                return False
            case 403:
                print(f'Forbidden: {response.request.url}: \n{content}')
                return False
            case 404:
                print(f'Unknown URL {response.request.url}: \n{content}')
                return False
            case _:
                print(f'Bad Request {response.request.url}: \n{content}')
                return False
