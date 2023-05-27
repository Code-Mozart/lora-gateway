import json


class DTO:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class DataDTO(DTO):
    def __init__(self, measuredAtTime, measurementType, measuredValue):
        self.measuredAt = measuredAtTime
        self.type = measurementType
        self.value = measuredValue


def update_decoder(obj):
    return UpdateDTO(obj['id'], obj['createdAt'], obj['updatedAt'], obj['data'], obj['version'])


class UpdateDTO(DTO):
    def __init__(self, id, createdAt, updatedAt, data, version):
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.data = data
        self.version = version

    def __str__(self):
        return f'id: {self.id}\n' \
               f'createdAt: {self.createdAt}\n' \
               f'updatedAt: {self.updatedAt}\n' \
               f'data: {self.data}\n' \
               f'version: {self.version}\n' \
               f'---------------------------'
