from dtos import DTO, DataDTO


class HopDTO:
    def __init__(self, timestamp: str, sender_uuid: str):
        self.timestamp = timestamp
        self.sender_uuid = sender_uuid

    def convert_to_dto(self) -> DTO:
        raise Exception('Please implement method')


class HopMeasurementContent:
    def __init__(self, measurement_type: str, value: str):
        self.measurement_type = measurement_type
        self.value = value


class HopPackage(HopDTO):
    def __init__(self, timestamp: str, sender_uuid: str, content: HopMeasurementContent):
        super().__init__(timestamp, sender_uuid)
        self.content = content

    def convert_to_dto(self) -> DTO:
        return DataDTO(
            self.timestamp,
            self.content.measurement_type,
            self.content.value
        )


def hop_package_decoder(obj):
    return HopPackage(
        obj['timestamp'],
        obj['sender_uuid'],
        HopMeasurementContent(
            obj['content']['type'],
            obj['content']['value']
        )

    )
