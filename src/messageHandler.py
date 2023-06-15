import json

import paths
from httpImpl import HttpImpl
from meshDtos import mesh_package_decoder, mesh_missing_block_decoder
from hopDtos import hop_package_decoder
from util import DataSplitter
from hopMessageConverter import parse_message, HopMessageResponse


# pass received byte array from lora to decode_message function.
# then call convert method which should check the topic of the message
# and convert the string into the correct dto object via decoder methods.
# those object should then be adjusted to the structure needed by the backend.
# layer between LoRa and backend. Handles (prints) all exceptions
class MessageHandler:
    def __init__(self, http_impl: HttpImpl, data_splitter: DataSplitter):
        self.http_impl = http_impl
        self.data_splitter = data_splitter

    def handle(self, message: str):
        raise Exception('please implement method handle!')

    def decode_message(self, byte_array) -> str:
        raise Exception('please implement method decode_message!')

    def encode_message(self, message: str):
        raise Exception('please implement method encode_message!')


class MessageHandlerMesh(MessageHandler):
    def decode_message(self, byte_array) -> str:
        message: str = ''
        for byte in byte_array:
            h = hex(byte)[2:]
            # print(h)
            # ignore new line (a) and whitespace (20)
            if h != 'a' and h != '20':
                message += bytes.fromhex(h).decode('ascii')

        return message

    def handle(self, message: str):
        message_json = json.loads(message)

        # TODO: might work
        topic: str = message_json['topic']

        # TODO: check for all known topics

        # '/v1/updates/missing'
        if topic == paths.missingUpdateTopic:
            try:
                missing_block = mesh_missing_block_decoder(message_json)
                return self.data_splitter.get_block(missing_block.content.missing_block_index)
            except Exception as e:
                print(str(e))
                return None

        # '/v1/backend/measurements'
        elif topic == paths.measurementTopic:
            try:
                measurement = mesh_package_decoder(message_json)
                data = measurement.convert_to_dto()

                # self.http_impl.post_node_data(measurement.uuid, data)
                print(f'New measurement for node {measurement.uuid}')

                return None

            except Exception as e:
                print(str(e))
                return None

        # invalid
        else:
            print(f'invalid Topic: {topic}')
            return None


class MessageHandlerHop(MessageHandler):
    def decode_message(self, byte_array) -> str:
        message_hex: str = ''
        for byte in byte_array:
            message_hex += hex(byte)[2:]

        return message_hex

    def encode_message(self, hex_string):
        byte_array = []
        for i in range(0, len(hex_string), 2):
            hex_char = hex_string[i:i+2]
            dec_char: int = int(hex_char, 16)
            byte_array.append(dec_char)

        return byte_array

    def handle(self, message: str):
        try:
            response_package, topic, payload = parse_message(message)

            # if there is no topic it was not a publish -> send respose back into network
            if topic is None:
                return self.encode_message(response_package.message)

            # if there is a topic, check which backend request is needed
            # '/v1/updates/missing'
            if topic == paths.missingUpdateTopic:
                pass

            # '/v1/backend/measurements'
            elif topic == paths.measurementTopic:
                measurement = hop_package_decoder(json.loads(payload))
                data = measurement.convert_to_dto()

                # self.http_impl.post_node_data(measurement.sender_uuid, data)
                print(f'New measurement for node {measurement.sender_uuid}')

                return self.encode_message(response_package.message)

            # invalid
            else:
                print(f'invalid Topic: {topic}')
                return None

        except Exception as e:
            print(str(e))
            return None

        return None
