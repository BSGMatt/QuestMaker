import qx
import functions

obj = qx.createQXObject("armTest.qx");
instrIdx = 0;
#print(obj.toString());
#Execute every instruction in the object. 
while (not(obj.flags['END'])):
    functions.Exec[obj.nextInstruction().name](obj, obj.getInstruction(obj.currentAddress));
