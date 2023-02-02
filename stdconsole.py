import console;
import sys;

#A Console class that relies on regular input streams, like terminal, pipe or file. 
class StandardConsole(console.Console):

    def __init__(self):
        self.inStream = sys.stdin;
        self.outStream = sys.stdout;
        self.errStream = sys.stderr;

    def write(self, errOrOut: int, data: str):
        if (errOrOut == console.ERROR):
            self.errStream.write(data);
        else:
            self.outStream.write(data);

    def read(self):
        self.inStream.read();