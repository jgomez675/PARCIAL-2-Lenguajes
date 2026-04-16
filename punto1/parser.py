import re
import json

class Parser:
    def parse(self, command):
        command = command.strip()

        insert = re.match(r'INSERT (\w+) (\{.*\})', command)
        if insert:
            return ("INSERT", insert.group(1), self.parse_object(insert.group(2)))

        find = re.match(r'FIND (\w+)( WHERE (.+))?', command)
        if find:
            if find.group(3):
                return ("FIND", find.group(1), self.parse_condition(find.group(3)))
            return ("FIND", find.group(1), None)

        update = re.match(r'UPDATE (\w+) SET (\w+) = (.+) WHERE (.+)', command)
        if update:
            return (
                "UPDATE",
                update.group(1),
                update.group(2),
                self.parse_value(update.group(3)),
                self.parse_condition(update.group(4))
            )

        delete = re.match(r'DELETE (\w+) WHERE (.+)', command)
        if delete:
            return ("DELETE", delete.group(1), self.parse_condition(delete.group(2)))

        return None

    def parse_object(self, text):
        text = text.replace(":", '":').replace("{", '{"').replace(", ", ', "')
        return json.loads(text)

    def parse_condition(self, text):
        match = re.match(r'(\w+)\s*(=|>|<)\s*(.+)', text)
        return match.group(1), match.group(2), self.parse_value(match.group(3))

    def parse_value(self, value):
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        try:
            return int(value)
        except:
            return value
