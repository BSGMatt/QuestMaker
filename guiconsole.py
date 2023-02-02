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
    textBox['state'] = 'disabled';
    textBox['relief'] = 'solid';
    textBox.pack();

    entryText = StringVar();
    entry = ttk.Entry(frame, textvariable=entryText);
    entry.pack();

    def __init__(self, windowName: str):
        super().__init__();
        self.window.title(windowName);

    def write(self, errOrOut: int, data: str):
        return super().write(data);
    
    def read(self):
        pass;

    def run(self):
        self.window.mainloop();

GUIConsole("QXEngine").run();
