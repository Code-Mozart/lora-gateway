from dtos import DTO, DataDTO


class MeshDTO:
    def convert_to_dto(self) -> DTO:
        raise Exception('Please implement method')


class MeshContent:
    def __init__(self, measurement_type: str, value: str):
        self.measurement_type = measurement_type
        self.value = value


class MeshMeasurement(MeshDTO):
    def __init__(self, topic: str, uuid: str, message_timestamp: str, content: MeshContent):
        self.topic = topic
        self.uuid = uuid
        self.message_timestamp = message_timestamp
        self.content = content

    def convert_to_dto(self) -> DTO:
        return DataDTO(
            self.message_timestamp,
            self.content.measurement_type,
            self.content.value
        )


def mesh_measurement_decoder(obj):
    return MeshMeasurement(
        obj['topic'],
        obj['uuid'],
        obj['messageTimestamp'],
        MeshContent(
            obj['content']['type'],
            obj['content']['value']
        )
    )
