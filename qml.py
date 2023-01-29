import re
#This file is for testing the parsing of a qml file
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

class QMLObject:
    def __init__(self, variables: list[Variable], instructions: list[str], labels: list[Label]):
        self.variables = variables;
        self.instructions = instructions;
        self.labels = labels;
        self.currentInstruction = 0;

    #Get the string representing an instruction at the given address.
    def getInstruction(self, address: int) -> str:
        if (address < 0 or address >= len(self.instructions)): 
            return "";
        return self.instructions[address];

    #Returns the string representing the current instruction, and then increments the instruction pointer. 
    def nextInstruction(self):
        self.currentInstruction += 1;
        return self.getInstruction(self.currentInstruction - 1);

    #Jumps to the instruction at the given label. 
    def jump(label: Label):
        currentInstruction = label.address;

    def jump(address: int):
        currentInstruction = address;

    def toString(self) -> str:
        ret = "VARIABLES:\n";
        for v in self.variables:
            ret += "\t" + v.toString() + "\n";
        ret += "LABELS:\n";
        for l in self.labels:
            ret += "\t" + l.toString() + "\n";
        ret += "INSTRUCTIONS:\n";
        for i in self.instructions:
            ret += "\t" + i + "\n";
        
        return ret;
        

#Pre-process phase: Find all of the variables and labels
def processVariables(file) -> list:
    regex = "#\S+\s+\S+\s+\"?.+\"?";
    tokens = re.findall(regex, file.read());
    vars = [];

    for s in tokens:
        varProperties = re.split("\s+", s, maxsplit=2);
        value = None;
        if (varProperties[0] == "#INT"):
            value = int(varProperties[2]);
        elif (varProperties[0] == "#STR"):
            value = varProperties[2][1:-1];
        elif (varProperties[0] == "#BOOL"):
            if (varProperties[2] == "TRUE"):
                value = True;
            else:
                value = False;
        vars.append(Variable(varProperties[1], varProperties[0][1::], value));
    return vars;

def createQMLObject(filename) -> QMLObject:
    f = open(filename, "r");
    vars = processVariables(f);
    f.seek(0);
    inst = [];
    lbs = [];

    instAddr = 0;
    regex = r"(?<!\")![^\s\[\]\"]+|\[.+\]";
    tokens = re.findall(regex, f.read());
    for x in range(0, len(tokens)):
        instrStr = re.match("\[.+\]", tokens[x]);
        if (instrStr):
            inst.append(instrStr.group(0));
            instAddr += 1;
        elif (x + 1 == len(tokens) or re.match("\[.+\]", tokens[x+1]) == None):
            raise InvalidLabelError(x, "Label not associated with valid instruction.");
        else:
            label = re.match("(?<!\")![^\s\[\]\"]+", tokens[x]);
            if (label): lbs.append(Label(label.group(0)[1::], instAddr));
            
    return QMLObject(vars, inst, lbs);


filename = "test.qml";
qmlObject = createQMLObject(filename);
print(qmlObject.toString());
