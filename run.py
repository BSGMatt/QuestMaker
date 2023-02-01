import qx
import sys
import functions

obj = qx.createQXObject(sys.argv[1]);
instrIdx = 0;
#print(obj.toString());
#Execute every instruction in the object.
print("All instructions:", file=sys.stderr); 
for i in obj.instructions:
    print("\t" + i.toString(), file=sys.stderr);

print("Begin program", file=sys.stderr);
while (not(obj.flags['END'])):
    inst = obj.nextInstruction();
    #print("\tRunning: " + inst.toString());
    functions.Exec[inst.name](obj, obj.getInstruction(obj.currentAddress));
