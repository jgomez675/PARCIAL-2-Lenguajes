class LL1Parser:
    def __init__(self):
        self.input = ""
        self.pos = 0

    def parse(self, string):
        self.input = string + "$"
        self.pos = 0
        return self.S() and self.current() == "$"

    def current(self):
        return self.input[self.pos]

    def match(self, char):
        if self.current() == char:
            self.pos += 1
            return True
        return False

    def S(self):
        if self.current() == 'a':
            return self.match('a') and self.match('b')
        elif self.current() == 'b':
            return self.match('b') and self.match('a')
        return False


if __name__ == "__main__":
    parser = LL1Parser()

    tests = ["ab", "ba", "aa", "bb", "aba"]

    for t in tests:
        result = parser.parse(t)
        print(f"{t} -> {'Válida' if result else 'Inválida'}")
