import json


class DTO:
    def to_json(self):
        raise Exception('Please implement method')


class DataDTO(DTO):
    def __init__(self, measured_at_time, measurement_type, measured_value,
                 backend_id=None, created_at=None):
        self.measuredAt = measured_at_time
        self.type = measurement_type
        self.value = measured_value
        self.backend_id = backend_id
        self.createdAt = created_at

    def to_json(self):
        body = json.dumps(self, default=lambda o: o.__dict__)
        body_dict = json.loads(body)
        body_dict.pop('backend_id')
        body_dict.pop('createdAt')
        return json.dumps(body_dict, default=lambda o: o.__dict__)


def data_decoder(obj):
    return DataDTO(
        obj['measuredAt'],
        obj['measuredAt'],
        obj['value'],
        obj['backend_id'],
        obj['createdAt']
    )


class BulkDataDTO(DTO):
    def __init__(self):
        self.bulk_data = []

    def append(self, data_dto: DataDTO):
        self.bulk_data.append(data_dto)

    def to_json(self):
        body = json.dumps(self, default=lambda o: o.__dict__)
        body_dict = json.loads(body)
        for item in body_dict['bulk_data']:
            item.pop('backend_id')
            item.pop('createdAt')
        return json.dumps(body_dict['bulk_data'], default=lambda o: o.__dict__)


def bulk_data_decoder():
    # implement when needed
    return None


class UpdateDTO(DTO):
    def __init__(self, update_id, created_at, updated_at, data, version):
        self.id = update_id
        self.createdAt = created_at
        self.updatedAt = updated_at
        self.data = data
        self.version = version

    def __str__(self):
        return f'id: {self.id}\n' \
               f'createdAt: {self.createdAt}\n' \
               f'updatedAt: {self.updatedAt}\n' \
               f'data: {self.data}\n' \
               f'version: {self.version}\n' \
               f'---------------------------'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def update_decoder(obj):
    return UpdateDTO(
        obj['id'],
        obj['createdAt'],
        obj['updatedAt'],
        obj['data'],
        obj['version']
    )
