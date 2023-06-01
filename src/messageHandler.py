import json

import dtos
from dtos import DTO

# pass received byte array via lora to decode_message function
# then call convert method which should check the topic of the message
# and convert the string into the correct dto object via decoder methods
class MessageHandler:
    def __init__(self):
        pass

    def convert(self):
        raise Exception('please implement method convert!')

    def decode_message(self, byte_array) -> str:
        message: str = ''
        for byte in byte_array:
            h = hex(byte)[2:]
            message += bytes.fromhex(h).decode('ascii')

        return message


class MessageHandlerMesh(MessageHandler):
    def convert(self, message: str) -> DTO:
        message_json = json.loads(message)

        # TODO: check for topic and return correct dto

        # used for testing
        return dtos.update_decoder(message_json)


class MessageHandlerHop(MessageHandler):
    def convert(self, message: str) -> DTO:
        message_json = json.loads(message)

        # TODO: check for topic and return correct dto

        # used for testing
        return dtos.update_decoder(message_json)
