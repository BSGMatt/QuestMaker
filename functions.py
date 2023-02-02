#This script features the implementation of the provided functions.
import re
import sys
import operator as op
from console import Console
from instruction import Instruction, Variable
from qx import QXObject

ArmOperators = {'ADD':op.add, 'SUB':op.sub, 'MUL':op.mul, 'DIV':op.floordiv};
Compare = {'EQ':op.eq, 'LE':op.le, 'GE':op.ge, 'LT':op.lt, 'GT':op.gt, 'NE':op.ne};

class QXRunner():

    def __init__(self, qx: QXObject, console: Console):
        self.qx = qx;
        self.console = console;

    def findVariable(q: QXObject, varName: str) -> Variable:
        for v in q.variables:
            if (("$" + v.name) == varName):
                return v;
        return None;

    def getValueOf(self, arg: str):
        if (arg.find('$') == 0):
            return int(self.findVariable(self.qx, arg).value);
        elif (arg.find('\"') == 0):
            return str(arg)[0:-1];
        elif (arg == 'TRUE'):
            return True;
        elif (arg == 'FALSE'):
            return False;
        else:
            return int(arg);

    def ARM(self, instr: Instruction):
        opFunc = ArmOperators[instr.args[0]];
        dest = 0; 
        srcA = 0;
        srcB = 0;
        if (instr.args[1].find('$') >= 0):
            dest = self.findVariable(q, instr.args[1]);

        if (instr.args[2].find('$') >= 0):
            srcA = int(self.findVariable(q, instr.args[2]).value);
        else:
            srcA = int(instr.args[2]);

        if (instr.args[3].find('$') > 0):
            srcB = int(self.findVariable(q, instr.args[3]).value);
        else:
            srcB = int(instr.args[3]);

        dest.value = opFunc(srcA, srcB);
        print(dest.toString(), file=sys.stderr);

    def JUMP(self, instr: Instruction):
        for l in self.qx.labels:
            if (l.label == instr.args[0]):
                self.qx.currentAddress = l.address - 1;

    def JUMPIF(self, instr: Instruction):
        if (Compare[instr.args[1]](self.getValueOf(self.qx, instr.args[2]), self.getValueOf(self.qx, instr.args[3]))):
            self.JUMP(qx, instr);

    def WAIT(self, instr: Instruction):
        numNops = self.getValueOf(self.qx, instr.args[0]);
        for i in range(numNops):
            self.qx.instructions.insert(self.qx.currentAddress + i + 1, Instruction("NOP", [0], qx.currentAddress + i + 1));

    def NOP(self, instr: Instruction):
        print("NOP", file=sys.stderr);
        self.qx.instructions.pop(self.qx.currentAddress);
        self.qx.currentAddress -= 1;

    def END(self, instr: Instruction):
        print("End of qx object.");
        self.qx.flags['END'] = True;

    Exec = {'ARM':ARM, 'END':END, 'JUMP':JUMP, 'JUMPIF':JUMPIF, 'WAIT':WAIT, 'NOP':NOP};