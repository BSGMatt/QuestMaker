import re
import sys
import copy
from instruction import *
#This script handles parsing text that uses the .qx format
class QXObject:
    
    flags = {'END':False, 'WAIT':False};

    def __init__(self, structs: list[Struct], variables: list[Variable], instructions: list[Instruction], labels: list[Label]):
        self.variables = variables;
        self.instructions = instructions;
        self.labels = labels;
        self.structs = structs;

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
        ret = "STRUCTS:\n";
        for s in self.structs:
            ret += "\t" + s.toString() + "\n";
        ret += "VARIABLES:\n";
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

    newArgRegex = r"(?<!\B\b\"[^\"])\s*[\(,)]\s*(?![^\"]*\"\B\b)";
    oldArgRegex = r"(?!\B\"[^\"]*)\s*[\(,)]\s*(?![^\"]*\"\B)";

    iName = re.search(r"\S+(?=\()", line).group(0);
    iArgs = re.split(oldArgRegex, line);
    return Instruction(iName, iArgs[1:-1], address);

def processStructs(file) -> list:
    startStructRegex = r"struct\s+(\w+)\s*";
    endStructRegex = r"end struct;";
    variableRegex = r"\w+\s+\S+;";

    starts = list(re.finditer(startStructRegex, file.read()));
    file.seek(0);
    ends = list(re.finditer(endStructRegex, file.read()));

    structs = [];

    if (len(starts) != len(ends)):
        raise VariableParseError("Failed to parse struct definitions [mismatch start and end lengths]");

    for i in range(len(starts)):

        #Parse the fields and the name of the struct. 
        varStr = starts[i].string[starts[i].end():ends[i].start()];
        structName = re.match(r"struct\s+(\w+)\s*", starts[i][0])[1];

        startIdx = starts[i].end();
        endIdx = ends[i].start();
    
        if (endIdx <= startIdx):
            raise VariableParseError("Failed to parse struct definitions [expected 'end struct']");

        #Parse out each of the struct's fields
        parses = re.findall(variableRegex, varStr);
        vars = []; 
        for p in parses:
            varIsStruct = False;
            varProperties = re.split(r"\s+=?\s*|=", p, maxsplit=2);
            value = None;
            if (varProperties[0] == "int"):
                value = 0;
            elif (varProperties[0] == "str"):
                value = "";
            elif (varProperties[0] == "bool"):
                value = False;
            else:
                #Assume variable is a struct. 
                value = "";
                varIsStruct = True;
            vars.append(Variable(varProperties[1].lstrip()[0:-1], varProperties[0], value, varIsStruct));
        newStruct = Struct(structName, vars);
        structs.append(newStruct);

    return structs;

def parseStruct(structList: list[Struct], structName: str, argString: str) -> Struct:
    
    #print("ARGSTRING: " +argString);

    splitRegex = r"[,{}];?";
    parseRegex = r"\"\w*\"|{.*}|\w+";
    assignRegex = r"\w+\s*=\s*\"?.+\"?";
    struct = createStruct(structName, structList);

    #print(struct);

    if (struct == None): return None;

    #Parse the string into separate args
    #Remove first and last entries since they're empty.
    argString = argString[1:-1];

    #If there are no args to be parsed, then return the struct as is. 
    if (argString == ''): return struct;
    args = re.findall(parseRegex, argString);

    print(args);

    i = 0;
    for a in args:
        arg = a.strip();
        if (arg == ''): continue;
        #Check if the arg is formatted as 'key = value'
        if (re.match(assignRegex, arg) != None):
            kv = re.split(r"\s*=\s*", arg);
            var = struct.getField(kv[0]);
            if (var != None):
                if (var.type == "int"):
                    var.value = int(kv[1]);
                elif(var.type == "str"):
                    var.value = str(kv[1])[1:-1];
                elif(var.type == "bool"):
                    if (kv[1] == "TRUE"): 
                        var.value = True;
                    else:
                        var.value = False;
                else:
                    var.isStruct = True;
                    var.value = parseStruct(structList, var.type, kv[1]);
        else:
            var = struct.fields[i];
            print(var);
            if (var.type == "int"):
                var.value = int(arg);
            elif(var.type == "str"):
                var.value = str(arg)[1:-1];
            elif(var.type == "bool"):
                if (arg == "TRUE"): 
                    var.value = True;
                else:
                    var.value = False;
            else:
                var.isStruct = True;
                var.value = parseStruct(structList, var.type, arg);
    
        i += 1;
    
    #print(struct);

    return struct;

#Creates an instance of a struct based on the templates in the given list. 
def createStruct(name: str, structList: list[Struct]) -> Struct:

    #print("structList: " + str(structList));

    for s in structList:
        if (s.name == name):
            #Copy the template of the list. 
            return copy.deepcopy(Struct(s.name, s.fields));

    return None;

#Pre-process phase: Find all of the variables and labels
def processVariables(file, structs: list[Struct]) -> list:
    regex = r"\w+\s+\S+\s*(?<![<>=])=\s*\"?.+\"?;";
    
    tokens = re.findall(regex, file.read());
    vars = [];
    for s in tokens:
        varIsStruct = False;
        varProperties = re.split(r"\s+=?\s*|=", s, maxsplit=2);
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
        else:
            #Create a struct object using the given argument string.
            value = parseStruct(structs, varProperties[0], re.search(r"{.*}", s)[0]);
            varIsStruct = True;
        vars.append(Variable(varProperties[1].lstrip(), varProperties[0], value, varIsStruct));
    return vars;

def toArmFunction(line: str, address: int) -> Instruction:

    #print(line);

    equalRegex = r"\B[=+-/*]\B";
    o = r"\s*[=+-/*]\s*";

    args = re.split(equalRegex, line);

    #Remove any trailing or leading whitespace. 
    for i in range(len(args)):
        args[i] = args[i].strip();

    args[-1] = args[-1][0:-1]; #Remove the ';' mark. 

    l = [];

    #If the instruction is a variable assignment. 
    if (len(args) == 2):
        return Instruction("ASSIGN", args, address);

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

def createQXObject(filename, addr = 0) -> QXObject:
    f = open(filename, "r");
    structs = processStructs(f); 

    #Define a struct for string and integer arrays.
    arr = [];
    for i in range(64):
        arr.append(Variable("["+str(i)+"]", "int", 0, False));
    structs.append(Struct("arr_int", arr));
    
    arr = [];
    for i in range(64):
        arr.append(Variable("["+str(i)+"]", "str", "", False));
    structs.append(Struct("arr_str", arr));

    f.seek(0);
    vars = processVariables(f, structs);

    #Define the return address variable. 
    vars.append(Variable("ra", "int", 0, False));

    f.seek(0);
    inst = [];
    lbs = [];

    instAddr = addr;
    regex = r"(?=\S).*;?";
    instrRegex = r"\S+(?=\()\(.*\)";
    labelRegex = r"#\w+"
    armRegex = r"\$\S+\s*=\s*.*;";
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

            
    return QXObject(structs, vars, inst, lbs);
