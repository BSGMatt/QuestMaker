import qx
import sys
import functions

obj = qx.createQXObject(sys.argv[1]);
instrIdx = 0;
#print(obj.toString());
#Execute every instruction in the object. 
while (not(obj.flags['END'])):
    functions.Exec[obj.nextInstruction().name](obj, obj.getInstruction(obj.currentAddress));
