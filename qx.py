import re
import sys
from instruction import Variable, Instruction, Label, InvalidLabelError
#This script handles parsing text that uses the .qx format

class QXObject:
    def __init__(self, variables: list[Variable], instructions: list[Instruction], labels: list[Label]):
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
            ret += "\t" + i.toString() + "\n";
        
        return ret;
        
def processInstruction(line: str, address: int) -> Instruction:
    iName = re.search(r"\S+(?=\()", line).group(0);
    iArgs = re.split(r"[\(,\);]", line);
    return Instruction(iName, iArgs[1:-1], address);

#Pre-process phase: Find all of the variables and labels
def processVariables(file) -> list:
    regex = r"\w+\s+\S+\s*=\s*\"?.+\"?;";
    
    tokens = re.findall(regex, file.read());
    vars = [];

    for s in tokens:
        varProperties = re.split("\s+=?\s*|=", s, maxsplit=2);
        value = None;
        if (varProperties[0] == "int"):
            value = int(varProperties[2][0:-1]);
        elif (varProperties[0] == "str"):
            value = varProperties[2][1:-2];
        elif (varProperties[0] == "bool"):
            if (varProperties[2][::-1] == "TRUE"):
                value = True;
            else:
                value = False;
        vars.append(Variable(varProperties[1], varProperties[0], value));
    return vars;

def toArmFunction(line: str, address: int) -> Instruction:
    args = re.split(r"\s*[=+-/*]\s*", line);
    args[-1] = args[-1][0:-1]; #Remove the ';' mark. 

    l = [];
    print(args[-1]);

    opName = 'DIV';
    if (line.find('+') > 0):
        opName = 'ADD';
    elif (line.find('-') > 0):
        opName = 'SUB';
    elif (line.find('*') > 0):
        opName = 'MUL';
    
    l.append(opName);
    l.extend(args);

    return Instruction("ARM", l, address);

def createQMLObject(filename) -> QXObject:
    f = open(filename, "r");
    vars = processVariables(f);
    f.seek(0);
    inst = [];
    lbs = [];

    instAddr = 0;
    regex = r"(?=\S).*;?";
    instrRegex = r"\S+(?=\()\(.*\)";
    labelRegex = r"#\w+"
    armRegex = r"\$\w+\s*=\s*.*;";

    tokens = re.findall(regex, f.read());
    for x in range(0, len(tokens)):
        instrStr = re.match(instrRegex, tokens[x]);
        if (instrStr):
            inst.append(processInstruction(instrStr.group(0), instAddr));
            instAddr += 1;
            continue;
        instrStr = re.match(labelRegex, tokens[x]);
        if (instrStr):
            #If the label isn't pointing to an instruction, raise an error.
            if (x + 1 == len(tokens) or re.match(instrRegex, tokens[x+1]) == None):
                raise InvalidLabelError(tokens[x], "Label not associated with valid instruction.");
            else:
                lbs.append(Label(instrStr.group(0)[1::], instAddr));
            continue;
        instrStr = re.match(armRegex, tokens[x]);
        if (instrStr):
            inst.append(toArmFunction(tokens[x], instAddr));
            instAddr += 1;
        #elif (x + 1 == len(tokens) or re.match("\w+(?=\()\(.*\)", tokens[x+1]) == None):
            #raise InvalidLabelError(x, "Label not associated with valid instruction.");
            #continue;
        #else:
            #label = re.match("#\w+", tokens[x]);
            #if (label): lbs.append(Label(label.group(0)[1::], instAddr));
            
    return QXObject(vars, inst, lbs);
