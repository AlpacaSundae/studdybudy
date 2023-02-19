from SoundRandomiser import *
from tkinter import *
import tkinter as tk
#import subprocess

class UserInterfaceError(Exception):
    pass

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.srSetup()
        self.mainMenu()

#
#   Main menu 
#
    def mainMenu(self):
        self.title("studdy budy 0.1")
        #self.geometry("300x120")

        label = tk.Label(self, text="main menu ? ?")
        label.pack()

        xsize, ysize = self.srMenu(label.winfo_reqheight())
        self.minsize(xsize, ysize + label.winfo_reqheight())

#
#   SoundRandomiser functions and menu\
#
#   srStart, and srStop are tied to GUI buttons
#   srSetup only needs be called once, for setup
#   srMenu is called each time the menu needs to be reopened.
    def srSetup(self):
        pygame.init()
        self.srLoop = False
        self.srPlayer = SoundRandomiser()
        self.srInterval = 100
        self.srPlayer.setProbability(0.0625)

    def srStart(self, start=False):
        if start and not self.srLoop:
            print("starting SoundRandomiser playback loop")
            self.srLoop = True
        if self.srLoop:
            self.srPlayer.roll()
            self.after(self.srInterval, self.srStart)

    def srStop(self):
        if self.srLoop:
            self.srLoop = False
            print("stopping SoundRandomiser playback loop")

#       opening this menu does not impact the flow of the sr functionality
#       INPUTS and optional offset for the height to palce the manu at
#           (allows for layering menus)
#       RETURNS the minimum required x and y size for the menu 
    def srMenu(self, offset=0):
        srLabel = tk.Label(self, text="Sound Randomiser")
        srLabel.place(
            anchor=N,
            relx=0.5,
            y=offset,
        )

        width = 64
        height = 32
        srButton = [
            tk.Button(self, text="Start", bg="blue", command=lambda: self.srStart(True)),
            tk.Button(self, text="Stop" , bg="blue", command=self.srStop),
        ]
        for ii, button in enumerate(srButton):
            xpos = width*(-len(srButton)*0.5+ii+0.5)

            button.place(
            anchor=N, 
            height=height, 
            width=width, 
            relx=0.5, 
            y=offset+height*2/3, 
            x=xpos,
        )

        # calc this menus min required size 
        minsize = [
            max(
                len(srButton) * width,
                srLabel.winfo_reqwidth()),
            height + srLabel.winfo_reqheight()
        ]

        return minsize



#   Current implementation has the app run from this script
#   unsure what functionality would cause this to change...
def main():
    UI = UserInterface()
    UI.mainloop()

if __name__ == "__main__":
    main()