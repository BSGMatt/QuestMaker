class Instruction:
    def __init__(self, name: str, args: list, address: int):
        self.name = name;
        self.args = args;
        self.address = address;
    def toString(self):
        return "[" + self.name + ":(" + str(len(self.args)) + " args) @" + str(self.address) + "]";

class Variable:
    def __init__(self, name: str, type: str, value):
        self.name = name;
        self.type = type;
        self.value = value;

    def toString(self) -> str:
        return "[" + self.name + ", " + self.type + ", " + str(self.value) + "]";

class Label:
    def __init__(self, label: str, address: int):
        self.label = label;
        self.address = address;
    def toString(self) -> str:
        return "[" + self.label + " @ Address: " + str(self.address) + "]";

class InvalidLabelError(ValueError):
    def __init__(self, label: str, message: str):
        self.label = label;
        self.message = message;
