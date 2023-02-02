import qx
import sys
import functions
import stdconsole as std;

qxRunner = QXRunner(qx.createQXObject(sys.argv[1]), std.StandardConsole());
#print(obj.toString());
#Execute every instruction in the object.
print("All instructions:", file=sys.stderr); 
for i in obj.instructions:
    print("\t" + i.toString(), file=sys.stderr);

print("Begin program", file=sys.stderr);
while (not(qxRunner.qx.flags['END'])):
    functions.Exec[qxRunner.qx.nextInstruction().name](qxRunner.qx.getInstruction(qxRunner.qx.currentAddress));
