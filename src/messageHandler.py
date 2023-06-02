import json

import paths
from httpImpl import HttpImpl
from meshDtos import mesh_measurement_decoder
from util import DataSplitter


# pass received byte array from lora to decode_message function.
# then call convert method which should check the topic of the message
# and convert the string into the correct dto object via decoder methods.
# those object should then be adjusted to the structure needed by the backend.
# layer between LoRa and backend. Handles (prints) all exceptions
class MessageHandler:
    def __init__(self, http_impl: HttpImpl, data_splitter: DataSplitter):
        self.http_impl = http_impl
        self.data_splitter = data_splitter
        pass

    def handle(self, message: str):
        raise Exception('please implement method handle!')

    def decode_message(self, byte_array) -> str:
        message: str = ''
        for byte in byte_array:
            h = hex(byte)[2:]
            # print(h)
            # ignore new line (a) and whitespace (20)
            if h != 'a' and h != '20':
                message += bytes.fromhex(h).decode('ascii')

        return message


class MessageHandlerMesh(MessageHandler):
    def handle(self, message: str):
        message_json = json.loads(message)

        # TODO: might work
        topic: str = message_json['topic']

        # TODO: check for all known topics
        match topic:

            # '/v1/updates/missing'
            case paths.missingUpdateTopic:

                # TODO: define DTO for this and extract missingBlockIndex
                block_index: int = 0
                # TODO: define DTO for sending a missing update and create and return this object here
                return self.data_splitter.get_block(block_index)

            # '/v1/backend/measurement'
            case paths.measurementTopic:

                try:
                    measurement = mesh_measurement_decoder(message_json)
                    data = measurement.convert_to_dto()

                    self.http_impl.post_node_data(measurement.uuid, data)
                    print(f'New measurement for node {measurement.uuid}')

                    return None

                except Exception as e:
                    print(str(e))
                    return None

            case _:
                print(f'invalid Topic: {topic}')
                return None


class MessageHandlerHop(MessageHandler):
    def handle(self, message: str):
        # TODO: adjust according to multi hop group specification
        return None
