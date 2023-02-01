class Instruction:
    def __init__(self, name: str, args: list[str], address: int):
        self.name = name;
        self.args = args;
        self.address = address;
    def toString(self):
        argStr = '';
        for i in self.args[0:-1]:
            argStr += (i + ", ");
        argStr += self.args[-1];
        return "[" + self.name + ": {" + argStr + "} @" + str(self.address) + "]";

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
