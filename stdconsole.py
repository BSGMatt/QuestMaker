import console;
import sys;

#A Console class that relies on regular input streams, like terminal, pipe or file. 
class StandardConsole(console.Console):

    def __init__(self):
        self.inStream = sys.stdin;
        self.outstream = sys.stdout;
        self.errStream = sys.stderr;

    def write(self, errOrOut: int, data: str):
        if (errOrOut == console.ERROR):
            stream = self.errStream;
        else:
            stream = self.outStream;
        stream.write(data);

    def read(self):
        self.instream.read();