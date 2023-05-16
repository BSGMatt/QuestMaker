from tkinter import *
from tkinter import ttk
import console;
import sys;
import re;

class GUIConsole(console.Console):

    text_scroll_speed = 100; #Number of ms between printing words to output. 
    ready_to_quit = False;
    
    oldData = "";

    def __init__(self, windowName = "QXEngine GUI"):
        super().__init__();
        self.window = Tk();
        self.window.title(windowName);
        self.window.geometry('640x480');
        self.window.protocol("WM_DELETE_WINDOW", self.quit);

        self.frame = ttk.Frame(self.window, padding=10);
        self.frame['relief'] = 'solid';
        self.frame.pack();

        self.textBox = Text(self.frame);
        self.textBox['state'] = 'normal';
        self.textBox['relief'] = 'solid';
        self.textBox.pack();

        entryText = StringVar();
        self.entry = ttk.Entry(self.frame, textvariable=entryText);
        self.entry.configure(width=120);
        self.entry.pack();

        #Handle user input from gui.
        self.entryButtonPressed = StringVar();
        self.entryButton = Button(self.frame, text="Enter", command=lambda: self.entryButtonPressed.set("Confirm"));
        self.entryButton.pack(side="right");
    
        

    def write(self, errOrOut: int, data: str):

        print(data, file=sys.stderr);
        if (errOrOut == 0):
            print(data, file=sys.stderr);
            return;

        self.textBox['state'] = 'normal';
        #Clear the text box and reinsert text once the text is beyond the box height. 
        self.textBox.insert('end', data);
        #print("END BEFORE: " + self.textBox.index('end'));
        if (int(self.textBox.index('end').split('.')[0]) >= self.textBox.cget('height')):
            self.textBox.delete('1.0','end');
            self.textBox.insert('end', self.oldData);
            self.textBox.insert('end', data);
        self.textBox['state'] = 'disabled';
        #print("END AFTER: " + self.textBox.index('end'));
        self.oldData = data;
        
        

    def printInputText(self):
        self.write(1, ">>" + self.entry.get() + "\n");

    def scrollPrintWords(self, words: list, wordIdx: int):

        #Stop when there's no longer any words to print. 
        if (wordIdx >= len(words)): return;

        self.textBox['state'] = 'normal';
        #Clear the text box and reinsert text once the text is beyond the box height. 
        self.textBox.insert('end', words[wordIdx] + " ");
        if (int(self.textBox.index('end').split('.')[0]) > self.textBox.cget('height')):
            self.textBox.delete('1.0','end');
            self.textBox.insert('end', words[wordIdx]);
        
        self.window.after(self.text_scroll_speed, self.scrollPrintWords, words, wordIdx + 1);
        self.textBox['state'] = 'disabled';
    
    def read(self):
        self.entryButton.wait_variable(self.entryButtonPressed);
        self.printInputText();
        inStr = self.entry.get();
        self.entry.delete('0', 'end');
        return inStr;

    def update(self):
        self.window.update_idletasks();
        self.window.update();
        

    def run(self):
        self.window.mainloop();

    def quit(self):
        self.ready_to_quit = True;
        self.entryButtonPressed.set("Confirm"); #Stop console from waiting for input
        self.window.destroy();

    def clear(self):
        self.textBox.delete('1.0','end');

        