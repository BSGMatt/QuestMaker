class Instruction:
    def __init__(self, name: str, args: list[str], address: int):
        self.name = name;
        self.args = args;
        self.address = address;

    def toString(self):
        argStr = '';
        for i in self.args[0:-1]:
            argStr += (str(i) + ", ");
        argStr += self.args[-1];
        return "[" + self.name + ": {" + argStr + "} @" + str(self.address) + "]";

    def __str__(self):
        return self.toString();

class Variable:
    def __init__(self, name: str, type: str, value, isStruct: bool):
        self.name = name;
        self.type = type;
        self.value = value;
        self.isStruct = isStruct;

    def toString(self) -> str:
        return "[" + self.name + ", " + self.type + ", " + str(self.value) + "]";

    def __str__(self):
        return self.toString();

class Struct:
    def __init__(self, name: str, fields: list[Variable]):
        self.name = name;
        self.fields = fields;

    def getField(self, name: str) -> Variable:

        print("GETTING FIELD OF NAME: " + name);

        split = name.split('.');

        for f in self.fields:
            if (f.name == split[0]):

                print("F.name: " + f.name);
                print(f);

                if (f.isStruct):
                    if (len(split) == 1):
                        return f;
                    return f.value.getField('.'.join(split[1::]));
                return f;
        return None;


    def toString(self) -> str:
        argStr = '';
        for i in self.fields[0:-1]:
            argStr += (str(i) + ", ");
        argStr += (str(self.fields[-1]));
        return self.name + ": {" + argStr + "}"; 

    def __str__(self):
        return self.toString();

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

class VariableParseError(SyntaxError):
    def __init__(self, message: str):
        self.message = message;
