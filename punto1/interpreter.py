from database import Database
from parser import Parser

class Interpreter:
    def __init__(self):
        self.db = Database()
        self.parser = Parser()

    def execute(self, command):
        parsed = self.parser.parse(command)

        if not parsed:
            return "[!] Comando no reconocido"

        if parsed[0] == "INSERT":
            return self.db.insert(parsed[1], parsed[2])

        if parsed[0] == "FIND":
            return self.db.find(parsed[1], parsed[2])

        if parsed[0] == "UPDATE":
            return self.db.update(parsed[1], parsed[2], parsed[3], parsed[4])

        if parsed[0] == "DELETE":
            return self.db.delete(parsed[1], parsed[2])
