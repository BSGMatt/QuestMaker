import re
#This file is for testing the parsing of a qml file
class Variable:
    def __init__(self, name: str, type: str, value):
        self.name = name;
        self.type = type;
        self.value = value;

qmlFile = open("test.qml", "r");

#Pre-process phase: Find all of the variables and labels
tokens = re.split("^(#\s+.\s+.\s+)", qmlFile.read());

for s in tokens:
    print(s + "\n");
    if ('\t' in s):
        print("There is a tab character here.\n");
