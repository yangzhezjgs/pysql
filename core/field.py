from pysql.core import FieldKey, FieldType, TYPE_MAP
from pysql.core import SerializedInterface

class Field(SerializedInterface):
    def __init__(self, data_type, keys=FieldKey.NULL, default=None):
        self.__type = data_type
        self.__keys = keys
        self.__default = default
        self.__values = []
        self.__rows = 0

    def add(self, value):
        if value is None:
            value = self.__default
        self.__values.append(value)
        self.__rows += 1

    def serialized(self):
        return SerializedInterface.json.dumps({
            'key': [key.value for key in self.__keys],
            'type': self.__type.value,
            'values': self.__values,
            'default': self.__default
        })

    @staticmethod
    def deserialized(data):
        json_data = SerializedInterface.json.loads(data)
        keys = [FieldKey(key) for key in json_data['key']]
        obj = Field(FieldType(json_data['type']), keys, default=json_data['default'])
        for value in json_data['values']:
            obj.add(value)
        return object
