import qx
import sys
import functions
import stdconsole as std;
import guiconsole as gui;

obj = qx.createQXObject(sys.argv[1]);
io = gui.GUIConsole("QXEngine UI");
qxRunner = functions.QXRunner(obj, io);
print(obj.toString(), file=qxRunner.console.outStream);
#Execute every instruction in the object.
print("All instructions:", file=sys.stderr); 
for i in qxRunner.qx.instructions:
    print("\t" + i.toString(), file=sys.stderr);

print("Begin program", file=sys.stderr);

while (not(qxRunner.qx.flags['END'])):
    qxRunner.Exec[qxRunner.qx.nextInstruction().name](qxRunner, qxRunner.qx.getInstruction(qxRunner.qx.currentAddress));
    io.window.update();

io.run();
