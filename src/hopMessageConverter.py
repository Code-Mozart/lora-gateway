def parse_message(message: str):
    # fixed header
    control_packet_type = message[0]
    control_flag = message[1]
    packet_length = message[2:4]

    message = message[4:]

    # connect
    if control_packet_type == '1':
        connect_message = ConnectMessage(message)
        return connect_message.handle()
    # publish
    elif control_packet_type == '3':
        publish_message = PublishMessage(message)
        return publish_message.handle()
    else:
        raise Exception(f'unsupported control packet type {control_packet_type}')


class HopMessageResponse:
    pass


class ConnectAck(HopMessageResponse):
    def __init__(self, return_code: str, network_id: str, uuid: str):
        self.message = f'{return_code}{network_id}{uuid}'


class PublishAck(HopMessageResponse):
    def __init__(self, packet_id: str):
        self.message = f'{packet_id}'


class HopMessage:

    def handle(self):
        raise Exception('Please implement handle method!')


# 1 byte = 2 chars
# control packet type == 1
class ConnectMessage(HopMessage):
    def __init__(self, message: str):
        self.protocol_version = None
        self.protocol_version_bytes = 1
        self.uuid = None
        self.uuid_bytes = 16
        self.message = message

    def handle(self):
        # 1 byte protocol version
        self.protocol_version = self.message[0:self.protocol_version_bytes * 2]
        self.message = self.message[self.protocol_version_bytes * 2:]

        # 16 bytes uuid
        self.uuid = self.message[self.uuid_bytes * 2:]

        return ConnectAck('00', '00', self.uuid), None, None


class PublishMessage(HopMessage):
    def __init__(self, message: str):
        self.topic_length = None
        self.topic_length_bytes = 1
        self.topic = None
        self.packet_id = None
        self.packet_id_bytes = 2
        self.payload = None
        self.message = message

    def handle(self):
        # 1 byte length of topic name
        self.topic_length = int(self.message[0:self.topic_length_bytes * 2], 16)
        self.message = self.message[self.topic_length_bytes * 2:]

        # x bytes for topic
        self.topic = self.message[0:self.topic_length * 2]
        self.message = self.message[self.topic_length * 2:]

        # 2 bytes for packet id
        self.packet_id = self.message[0:self.packet_id_bytes * 2]
        self.message = self.message[self.packet_id_bytes * 2:]

        # remaining bytes for payload
        self.payload = self.message[0:]

        return PublishAck(self.packet_id), \
            bytes.fromhex(self.topic).decode('ascii'), \
            bytes.fromhex(self.payload).decode('ascii')
