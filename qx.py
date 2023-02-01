import re
import sys
from instruction import Variable, Instruction, Label, InvalidLabelError
#This script handles parsing text that uses the .qx format

class QXObject:
    
    flags = {'END':False};

    def __init__(self, variables: list[Variable], instructions: list[Instruction], labels: list[Label]):
        self.variables = variables;
        self.instructions = instructions;
        self.labels = labels;

        self.currentAddress = -1;

    #Get the string representing an instruction at the given address.
    def getInstruction(self, address: int) -> Instruction:
        if (address < 0 or address >= len(self.instructions)): 
            return Instruction("END", [], -1);
        return self.instructions[address];

    #Returns the string representing the current instruction, and then increments the instruction pointer. 
    def nextInstruction(self):
        self.currentAddress += 1;
        return self.getInstruction(self.currentAddress);

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
    iArgs = re.split(r"\s*[\(,\)]\s*;*", line);
    return Instruction(iName, iArgs[1:-1], address);

#Pre-process phase: Find all of the variables and labels
def processVariables(file) -> list:
    regex = r"\w+\s+\S+\s*(?<![<>=])=\s*\"?.+\"?;";
    
    tokens = re.findall(regex, file.read());
    vars = [];
    for s in tokens:
        varProperties = re.split("\s+=?\s*|=", s, maxsplit=2);
        value = None;
        if (varProperties[0] == "int"):
            value = int(varProperties[2][0:-1]);
        elif (varProperties[0] == "str"):
            value = varProperties[2][0:-1];
        elif (varProperties[0] == "bool"):
            if (varProperties[2][::-1] == "TRUE"):
                value = True;
            else:
                value = False;
        vars.append(Variable(varProperties[1].lstrip(), varProperties[0], value));
    return vars;

def toArmFunction(line: str, address: int) -> Instruction:
    args = re.split(r"\s*[=+-/*]\s*", line);
    args[-1] = args[-1][0:-1]; #Remove the ';' mark. 

    l = [];

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

def toJumpIf(line: str, address: int) -> Instruction:
    regex = r"[,\(\s\);]+"
    lineArgs = re.split(regex, line);

    cCode = {'==':'EQ', '<=':'LE', '>=':'GE', '<':'LT', '>':'GT', '!=':'NE'};
    args = [];
    args.append(lineArgs[1]);
    args.append(cCode[lineArgs[3]]);
    args.append(lineArgs[2]);
    args.append(lineArgs[4]);
    return Instruction(lineArgs[0], args, address);

def createQXObject(filename) -> QXObject:
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
    compRegex = r"\S+\s*[<>=]=\s*\S+";

    tokens = re.findall(regex, f.read());
    for x in range(0, len(tokens)):
        instrStr = re.match(armRegex, tokens[x]);
        if (instrStr):
            #print("\t token being converted to ARM function");
            inst.append(toArmFunction(tokens[x], instAddr));
            instAddr += 1;
            continue;
        instrStr = re.search(compRegex, tokens[x]);
        if (instrStr):
            #print("\t token being converted to JUMPIF function");
            inst.append(toJumpIf(tokens[x], instAddr));
            instAddr += 1;
            continue;
        instrStr = re.match(instrRegex, tokens[x]);
        if (instrStr):
            #print("\t token being converted to standard function");
            inst.append(processInstruction(instrStr.group(0), instAddr));
            instAddr += 1;
            continue;
        instrStr = re.match(labelRegex, tokens[x]);
        if (instrStr):
            #print("\t token being converted to a label");
            #If the label isn't pointing to an instruction, raise an error.
            if (x + 1 == len(tokens) or re.match(labelRegex, tokens[x+1]) != None):
                raise InvalidLabelError(tokens[x], "Label not associated with valid instruction.");
            else:
                lbs.append(Label(instrStr.group(0)[1::], instAddr));
            continue;

            
    return QXObject(vars, inst, lbs);
