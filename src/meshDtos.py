from dtos import DTO, DataDTO


class MeshDTO:
    def __init__(self, topic: str, uuid: str, message_timestamp: str):
        self.topic = topic
        self.uuid = uuid
        self.message_timestamp = message_timestamp

    def convert_to_dto(self) -> DTO:
        raise Exception('Please implement method')


class MeshMeasurementContent:
    def __init__(self, measurement_type: str, value: str):
        self.measurement_type = measurement_type
        self.value = value


class MeshMissingBlockContent:
    def __init__(self, missing_block_index: int):
        self.missing_block_index = missing_block_index


class MeshPackage(MeshDTO):
    def __init__(self, topic: str, uuid: str, message_timestamp: str, content: MeshMeasurementContent):
        super().__init__(topic, uuid, message_timestamp)
        self.content = content

    def convert_to_dto(self) -> DTO:
        return DataDTO(
            self.message_timestamp,
            self.content.measurement_type,
            self.content.value
        )


class MeshMissingBlock(MeshDTO):
    def __init__(self, topic: str, uuid: str, message_timestamp: str, content: MeshMissingBlockContent):
        super().__init__(topic, uuid, message_timestamp)
        self.content = content

    def convert_to_dto(self) -> DTO:
        return None


def mesh_package_decoder(obj):
    return MeshPackage(
        obj['topic'],
        obj['uuid'],
        obj['messageTimestamp'],
        MeshMeasurementContent(
            obj['content']['type'],
            obj['content']['value']
        )
    )


def mesh_missing_block_decoder(obj):
    return MeshMissingBlock(
        obj['topic'],
        obj['uuid'],
        obj['messageTimestamp'],
        MeshMissingBlockContent(
            int(obj['content']['missingBlockIndex'])
        )
    )
