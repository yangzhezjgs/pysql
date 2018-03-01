from pysql.core import SerializedInterface
from pysql.core.field import Field

class Table(SerializedInterface):
    def __init__(self, **options):
        self.__field_names = []
        self.__field_objs = {}
        self.__rows = 0

        for field_name, field_obj in options.items():
            self.add_field(field_name, field_obj)

    def add_field(self, field_name, field_obj, value=None):
        self.__field_names.append(field_name)
        self.__field_objs[field_name] = field_obj

    def serialized(self):
        data = {}
        for field in self.__field_names:
            data[field] = self.__field_objs[field].serialized()
        return SerializedInterface.json.dumps(data)

    @staticmethod
    def deserialized(data):
        json_data = SerializedInterface.json.loads(data)
        table_obj = Table()
        field_names = [field_name for field_name in json_data.keys()]
        for field_name in field_names:
            field_obj = Field.deserialized(json_data[field_name])
            table_obj.add_field(field_name, field_obj)
        return table_obj
