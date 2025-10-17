import qx
import sys
import functions
import stdconsole as std;
import guiconsole as gui;

windowName = "QXEngine UI";

#Check if a file is given as an argument.
if (len(sys.argv) != 2):
    print("Proper usage: run.py [qxFileName]");
    exit();

obj = qx.createQXObject(sys.argv[1]);
io = gui.GUIConsole();
qxRunner = functions.QXRunner(obj, io);
print(obj.toString(), file=qxRunner.console.outStream);
#Execute every instruction in the object.
print("All instructions:", file=sys.stderr); 
for i in qxRunner.qx.instructions:
    print("\t" + i.toString(), file=sys.stderr);

print("Begin program", file=sys.stderr);
while (not(qxRunner.qx.flags['END'])):
    qxRunner.Execute(qxRunner.qx.nextInstruction().name, qxRunner.qx.getInstruction(qxRunner.qx.currentAddress));
    #io.update();


io.run();
sys.exit();


