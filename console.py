
ERROR = 0;
OUT = 1;

class Console:
    inStream = None;
    outStream = None;
    errStream = None;

    def __init__(self, inStream, outStream, errStream):
        self.inStream = inStream;
        self.outStream = outStream;
        self.errStream = errStream;

    def __init__(self):
        pass;

    #Read input from the console.
    def read(self):
        pass;
    
    #Writes to console. 
    def write(self, errOrOut: int, data: str):
        pass;

    #Quit the program
    def quit(self):
        pass;

    #Clear the screen.
    def clear(self):
        pass;