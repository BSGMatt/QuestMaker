#This script features the implementation of the provided functions.
import re
import sys
import operator as op
from instruction import Instruction, Variable
from qx import QXObject


ArmOperators = {'ADD':op.add, 'SUB':op.sub, 'MUL':op.mul, 'DIV':op.floordiv};
Compare = {'EQ':op.eq, 'LE':op.le, 'GE':op.ge, 'LT':op.lt, 'GT':op.gt, 'NE':op.ne};

def findVariable(q: QXObject, varName: str) -> Variable:
    for v in q.variables:
        if (("$" + v.name) == varName):
            return v;
    return None;

def getValueOf(q: QXObject, arg: str):
    if (arg.find('$') == 0):
        return int(findVariable(q, arg).value);
    elif (arg.find('\"') == 0):
        return str(arg)[0:-1];
    elif (arg == 'TRUE'):
        return True;
    elif (arg == 'FALSE'):
        return False;
    else:
        return int(arg);

def ARM(q: QXObject, instr: Instruction):
    opFunc = ArmOperators[instr.args[0]];
    dest = 0; 
    srcA = 0;
    srcB = 0;
    if (instr.args[1].find('$') >= 0):
        dest = findVariable(q, instr.args[1]);

    if (instr.args[2].find('$') >= 0):
        srcA = int(findVariable(q, instr.args[2]).value);
    else:
        srcA = int(instr.args[2]);

    if (instr.args[3].find('$') > 0):
        srcB = int(findVariable(q, instr.args[3]).value);
    else:
        srcB = int(instr.args[3]);

    dest.value = opFunc(srcA, srcB);
    print(dest.toString(), file=sys.stderr);

def JUMP(qx: QXObject, instr: Instruction):
    for l in qx.labels:
        if (l.label == instr.args[0]):
            qx.currentAddress = l.address - 1;

def JUMPIF(qx: QXObject, instr: Instruction):
    if (Compare[instr.args[1]](getValueOf(qx, instr.args[2]), getValueOf(qx, instr.args[3]))):
        JUMP(qx, instr);

def END(qx: QXObject, instr: Instruction):
    print("End of qx object.");
    qx.flags['END'] = True;

Exec = {'ARM':ARM, 'END':END, 'JUMP':JUMP, 'JUMPIF':JUMPIF};