from tkinter import *
from tkinter import ttk
import console;
import sys;

class GUIConsole(console.Console):

    window = Tk();
    window.geometry('640x480');

    frame = ttk.Frame(window, padding=10);
    frame['relief'] = 'solid';
    frame.pack();

    textBox = Text(frame);
    textBox['state'] = 'normal';
    textBox['relief'] = 'solid';
    textBox.pack();

    entryText = StringVar();
    entry = ttk.Entry(frame, textvariable=entryText);
    entry.configure(width=120);
    entry.pack();

    def __init__(self, windowName: str):
        super().__init__();
        self.window.title(windowName);

    def write(self, errOrOut: int, data: str):
        self.textBox['state'] = 'normal';
        self.textBox.insert('end', data);
        self.textBox['state'] = 'disabled';
    
    def read(self):
        inStr = input("");
        self.write(1, ">>" + inStr + "\n");
        return inStr;

    def run(self):
        self.window.mainloop();