#This script features the implementation of the provided functions.
import re
import sys
import operator as op
from console import Console
from instruction import *
from qx import QXObject
import random

ArmOperators = {'ADD':op.add, 'SUB':op.sub, 'MUL':op.mul, 'DIV':op.floordiv};
Compare = {'EQ':op.eq, 'LE':op.le, 'GE':op.ge, 'LT':op.lt, 'GT':op.gt, 'NE':op.ne};
EscapeChars = {'\\n':'\n', '\\t':'\t', '\\\\':'\\', '\\\"':'\"', '\\.':'.'};
varReferenceRegex = r"\$\w+\.?(?:[\w.]+|\[[^\]]+\])?";
inlineStringParseRegex = r"\$\{([^}]+)\}";

class QXRunner():

    def __init__(self, qx: QXObject, console: Console):
        self.qx = qx;
        self.console = console;


    #Finds a variable that being referenced within the qx script. 
    #varName must start with a '$' symbol. 
    def findVariable(self, varName: str) -> Variable:
        print("FINDING VARIABLE: " + varName);

        #Remove the '$' sign
        vName = varName[1::];

        if (vName in self.qx.variables.keys()):
            return self.qx.variables[vName]

        try:
            val = self.qx.variables[vName]
        except (AttributeError, KeyError, TypeError) as e:
            self.ThrowError(self.currentInstruction(), e)

        return None;

    def currentInstruction(self) -> Instruction:
        return self.qx.instructions[self.qx.currentAddress];

    def getValueOf(self, arg: str):
        if (arg in self.qx.variables.keys()):
            return self.qx.variables[arg].value;
        elif (arg.find('$') == 0):
            return self.findVariable(arg).value;
        elif (arg.find('\"') == 0):
            return str(arg)[1:-1];
        elif (arg == 'TRUE'):
            return True;
        elif (arg == 'FALSE'):
            return False;
        else:
            return float(arg);

    def ARM(self, instr: Instruction):

        typeOf = int;

        opFunc = ArmOperators[instr.args[0]];
        dest = 0; 
        srcA = 0;
        srcB = 0;
        if (instr.args[1].find('$') >= 0):
            dest = self.findVariable(instr.args[1]);
        
        srcA = self.getValueOf(instr.args[2]);
        srcB = self.getValueOf(instr.args[3]);

        try:
            dest.value = opFunc(srcA, srcB);
        except TypeError as t:
            self.ThrowError(instr, t);
        #print(dest.toString(), file=sys.stderr);

    def ASSIGN(self, instr: Instruction):
        if (instr.args[0].find('$') >= 0):
            dest = self.findVariable(instr.args[0]);
        if (instr.args[1].find('$') >= 0):
            srcA = self.findVariable(instr.args[1]).value;
        else:
            if (dest.type == 'str'):
                val = instr.args[1][1:-1];
            else:
                val = int(instr.args[1]);
            srcA = val;
    
        dest.value = srcA;
    
    def RAND(self, instr: Instruction):

        #Check if the client code is referencing an already created variable. 
        #If not, create one. 

        if (instr.args[0].find('$') >= 0):
            dest = self.findVariable(instr.args[0]);
        else:
            dest = Variable(instr.args[0], 'int', 0, False);
            self.qx.variables.append(dest);
        
        if (instr.args[1].find('$') >= 0):
            min = self.findVariable(instr.args[1]).value;
        else:
            min = int(instr.args[1]);
        if (instr.args[2].find('$') >= 0):
            max = self.findVariable(instr.args[2]).value;
        else:
            max = int(instr.args[2]);
        
        dest.value = random.randint(min, max);
        
        return;
        

    def DISP(self, instr: Instruction):
        #Find all of the variables embedded into the string.
        data = instr.args[0][1:-1];
        vars = list(re.finditer(inlineStringParseRegex, data));
        esc = re.findall(r"\\.", data);
        for v in vars:
            data = data.replace(v[0], str(self.getValueOf(v[1])), 1);
        for e in esc:
            data = data.replace(e, EscapeChars[e]);
        self.console.write(1, data);

    def PROMPT(self, instr: Instruction):

        #print(instr.args);
        #Display the prompt message. 
        self.DISP(Instruction("", [instr.args[1]], 0));

        if (instr.args[0].find('$') == 0):
            var = self.findVariable(instr.args[0]);
            if (var.type != "str"):
                raise TypeError("Expected 'str' but recieved variable of type: " + var.type);
            else:
                var.value = self.console.read();
                return;
        else:
            newVar = Variable(instr.args[0], 'str', "", False);
            self.qx.variables[newVar.name] = newVar;
            instr.args[0] = '$' + instr.args[0]; #Add the '$' to let the runner know that the variable has already been created. 
            newVar.value = self.console.read();
    
    def PROMPTEMPTY(self, instr: Instruction):
        self.PROMPT(Instruction("", [instr.args[0], ""], instr.address));

    def PROMPTINT(self, instr: Instruction):

        #print(instr.args);

        #Display the prompt message. 
        self.DISP(Instruction("", [instr.args[1]], 0));

        if (instr.args[0].find('$') == 0):
            var = self.findVariable(instr.args[0]);
            if (var.type != "int"):
                raise TypeError("Expected 'str' but recieved variable of type: " + var.type);
            else:
                var.value = int(self.console.read());
                return;
        else:
            newVar = Variable(instr.args[0], 'int', 0, False);
            self.qx.variables.append(newVar);
            instr.args[0] = '$' + instr.args[0]; #Add the '$' to let the runner know that the variable has already been created. 
            newVar.value = int(self.console.read());

    def JUMP(self, instr: Instruction):
        for l in self.qx.labels:
            if (l.label == instr.args[0]):
                self.qx.currentAddress = l.address - 1;

    def JUMPRET(self, instr: Instruction):
        self.findVariable("$ra").value = self.qx.currentAddress;
        self.JUMP(instr);

    def RETURN(self, instr: Instruction):
        self.qx.currentAddress = self.findVariable("$ra").value;

    def JUMPIF(self, instr: Instruction):
        if (Compare[instr.args[1]](self.getValueOf(instr.args[2]), self.getValueOf(instr.args[3]))):
            self.JUMP(instr);

    def WAIT(self, instr: Instruction):
        numNops = self.getValueOf(instr.args[0]);
        for i in range(numNops):
            self.qx.instructions.insert(self.qx.currentAddress + i + 1, Instruction("NOP", [0], self.qx.currentAddress + i + 1));

    def NOP(self, instr: Instruction):
        #print("NOP", file=sys.stderr);
        self.qx.instructions.pop(self.qx.currentAddress);
        self.qx.currentAddress -= 1;

    def END(self, instr: Instruction):
        print("End of qx object.", file=sys.stderr);
        self.qx.flags['END'] = True;
    
    def ThrowError(self, instr: Instruction, e):
        print("Instruction Failed!");
        print("Instruction: ", instr, e);
        self.END(instr);
    
    def CLEAR(self, instr: Instruction):
        self.console.clear();
    
    def Execute(self, instrName : str, instr: Instruction):
        if (instrName in self.Exec):
            self.Exec[instrName](self, instr);
        else:
            print("Could not find instruction: ", instrName);
            self.END(instr);

    Exec = {'ARM':ARM, 
            'END':END, 
            'JUMP':JUMP, 
            'JUMPIF':JUMPIF,
            'JUMPRET':JUMPRET,
            'RETURN':RETURN, 
            'WAIT':WAIT, 
            'NOP':NOP,
            'DISP':DISP,
            'PROMPT':PROMPT,
            'PROMPTINT':PROMPTINT,
            'PROMPTEMPTY':PROMPTEMPTY,
            'CLEAR':CLEAR,
            'ASSIGN':ASSIGN,
            'RAND':RAND};