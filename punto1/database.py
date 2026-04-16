import json

class Database:
    def __init__(self):
        self.data = {}

    def insert(self, collection, obj):
        if collection not in self.data:
            self.data[collection] = []
        self.data[collection].append(obj)
        return f"Insertado en '{collection}'"

    def find(self, collection, condition=None):
        if collection not in self.data:
            return "Colección no existe"

        results = []

        for record in self.data[collection]:
            if condition:
                field, operator, value = condition
                if self.evaluate(record, field, operator, value):
                    results.append(record)
            else:
                results.append(record)

        return json.dumps(results, indent=4, ensure_ascii=False)

    def update(self, collection, field, new_value, condition):
        if collection not in self.data:
            return "Colección no existe"

        count = 0

        for record in self.data[collection]:
            cond_field, operator, cond_value = condition
            if self.evaluate(record, cond_field, operator, cond_value):
                record[field] = new_value
                count += 1

        return f"{count} registros actualizados"

    def delete(self, collection, condition):
        if collection not in self.data:
            return "Colección no existe"

        new_data = []
        count = 0

        for record in self.data[collection]:
            field, operator, value = condition
            if self.evaluate(record, field, operator, value):
                count += 1
            else:
                new_data.append(record)

        self.data[collection] = new_data
        return f"{count} registros eliminados"

    def evaluate(self, record, field, operator, value):
        if field not in record:
            return False
        if operator == "=":
            return record[field] == value
        if operator == ">":
            return record[field] > value
        if operator == "<":
            return record[field] < value
        return False
