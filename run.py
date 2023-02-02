import qx
import sys
import functions
import stdconsole as std;

obj = qx.createQXObject(sys.argv[1]);
qxRunner = functions.QXRunner(obj, std.StandardConsole());
#print(obj.toString());
#Execute every instruction in the object.
print("All instructions:", file=sys.stderr); 
for i in qxRunner.qx.instructions:
    print("\t" + i.toString(), file=sys.stderr);

print("Begin program", file=sys.stderr);
while (not(qxRunner.qx.flags['END'])):
    qxRunner.Exec[qxRunner.qx.nextInstruction().name](qxRunner, qxRunner.qx.getInstruction(qxRunner.qx.currentAddress));
