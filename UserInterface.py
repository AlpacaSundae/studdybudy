from SoundRandomiser import *
from SoundLooper import *
from tkinter import *
import tkinter as tk
#import subprocess

SL_DIR = "audio/play/nirvana01.mp3"

class UserInterfaceError(Exception):
    pass

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.srSetup()
        self.slSetup()
        self.mainMenu()

    def errorMessage(self, msg):
        print(msg)
        self.status['text'] = msg

    def statusMessage(self, msg):
        print(msg)
        self.status['text'] = msg

#   given a list of buttons, place them in a centered row in the gui
    def centeredButtonRow(self, button_list, height=32, width=64, offset=0):
        for ii, button in enumerate(button_list):
            xpos = width*(-len(button_list)*0.5+ii+0.5)

            button.place(
            anchor=N, 
            height=height, 
            width=width, 
            relx=0.5, 
            y=offset, 
            x=xpos,
        )
        return [width*len(button_list), height] # [width, height] of button row

#   print pairs of label and entry box
#   width refers text box width
    def alignedTextPairColumn(self, label_list, entry_list, height=32, width=128, align=0, offset=0, padding=4):
        textpad = 6
        widest = 0
        altoffset = 0
        for label, entry in zip(label_list, entry_list):
            label.place(
                anchor=E, 
                relx=0.5, 
                y=altoffset+offset+height/2,
                x=-align
            )
            entry.place(
                anchor=NW, 
                height=height, 
                width=width, 
                relx=0.5, 
                y=altoffset+offset, 
                x=textpad-align,
            )

            widest = max(widest, label.winfo_reqwidth())

            altoffset += height + padding
            
        width = 2*max((width-align+8), align+textpad+widest)
        return [width, altoffset]


#   determine new bounds of two vertically aligned elements
    def newBoundsVertical(self, dim1, dim2):
        return [
            max(dim1[0], dim2[0]),  # width is the biggest width
            dim1[1] + dim2[1]       # height is the addition of heights
        ]

#
#   Main menu 
#
    def mainMenu(self):
        self.title("studdy budy 1.0")
        #self.geometry("300x120")

        label = tk.Label(self, text="main menu ? ?")
        label.pack()

        spacing = 12
        dimsCur = [0, label.winfo_reqheight()]
        
        dimsCur[1] += spacing
        dimsNew = self.srMenu(dimsCur[1])
        dimsCur = self.newBoundsVertical(dimsCur, dimsNew)

        dimsCur[1] += spacing
        dimsNew = self.slMenu(dimsCur[1])
        dimsCur = self.newBoundsVertical(dimsCur, dimsNew)

        dimsCur[1] += spacing
        dimsNew = self.status(dimsCur[1])
        dimsCur = self.newBoundsVertical(dimsCur, dimsNew)
        
        self.minsize(dimsCur[0], dimsCur[1])

    def status(self, offset):
        self.status = tk.Label(self, text="welcome!")
        self.status.pack(anchor = "s", side = LEFT)
        return [0, self.status.winfo_reqheight()]

#
#   SoundRandomiser functions and menu
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
            self.statusMessage("starting SoundRandomiser playback loop")
            self.srLoop = True
        if self.srLoop:
            self.srPlayer.roll()
            self.after(self.srInterval, self.srStart)

    def srStop(self):
        if self.srLoop:
            self.srLoop = False
            self.statusMessage("stopping SoundRandomiser playback loop")

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
        dim1 = [srLabel.winfo_reqwidth(), srLabel.winfo_reqheight()]

        srButton = [
            tk.Button(self, text="Start", bg="blue", command=lambda: self.srStart(True)),
            tk.Button(self, text="Stop" , bg="blue", command=self.srStop),
        ]
        dim2 = self.centeredButtonRow(srButton, offset=offset+srLabel.winfo_reqheight())

        # calc this menus min required size and return
        return self.newBoundsVertical(dim1, dim2)

#
#   SoundLooper functions and menu
#
    def slSetup(self):
        self.slMenuSetup()
        self.slPlayer = None
        self.slBounds = None
        self.slDisplayFrames = True
        self.slInterval = 1
        self.slPlaying = False
        self.slStopping = False
        self.slLooping = False

    def slLoadSong(self):
        filename = self.slFileSel[1][0].get()
        self.slBounds = None
        try:
            self.slPlayer = SoundLooper(filename)
            self.statusMessage(f"loaded: {filename}")
        except SoundLooperError as e:
            self.slPlayer = None
            self.errorMessage(e)

    def slLoadAuto(self):
        self.slLoadSong()
        self.slAutoBounds()
        self.slPlay(pressed=True)

    def slReadBounds(self):
        return [
            int(self.slLoopSel[1][0].get()),
            int(self.slLoopSel[1][1].get()),
        ]

    def slBoundSet(self, auto=True):
        if self.slPlayer:
            try:
                if auto:
                    self.slPlayer.autoset_looping()
                    self.slBounds = self.slPlayer.get_looping()
                else:
                    self.slBounds = self.slReadBounds()
                    self.slPlayer.set_looping(self.slBounds[0], self.slBounds[1])
                self.slSongLength = self.slPlayer.get_song_length()
                self.slToggleLoop(True)
                self.slDisplayBounds()
            except SoundLooperError as e:
                self.slBounds = [0, 0]
                self.errorMessage(e)
        else:
            self.errorMessage("No song is currently loaded")

    def slAutoBounds(self):
        self.slBoundSet(auto=True)

    def slManualBounds(self):
        self.slBoundSet(auto=False)

    def slDisplayBounds(self):
        self.slLoopSel[1][0].delete(0, END)
        self.slLoopSel[1][1].delete(0, END)
        self.slLoopSel[1][2].delete(0, END)
        if self.slDisplayFrames:
            self.slLoopSel[1][0].insert(END, self.slBounds[0])
            self.slLoopSel[1][1].insert(END, self.slBounds[1])
            self.slLoopSel[1][2].insert(END, self.slSongLength)
        else:
            self.slLoopSel[1][0].insert(END, self.slPlayer.frames_to_ftime(self.slBounds[0]))
            self.slLoopSel[1][1].insert(END, self.slPlayer.frames_to_ftime(self.slBounds[1]))
            self.slLoopSel[1][2].insert(END, self.slPlayer.frames_to_ftime(self.slSongLength))

    def slPlay(self, pressed=False):
        if pressed:
            self.slPlaying = True
        if self.slPlayer:
            try:
                self.slPlayer.play_looping_update(self.slLooping)
                if self.slStopping:
                    self.slPlaying = False
                    self.slStopping = False
                    self.slPlayer.set_looping(self.slBounds[0], self.slBounds[1])
                elif self.slPlaying:
                    self.after(self.slInterval, self.slPlay)
            except SoundLooperFinished:
                self.slPlaying = False
                self.statusMessage("Song finished")
        else:
            self.errorMessage("No song loaded to play")

    def slPause(self):
        self.slPlaying = False

    def slStop(self):
        self.slStopping = True

    def slToggleLoop(self, set=False):
        if set:
            self.slLooping = True
        else:
            self.slLooping = not self.slLooping
        self.slButtons[1][3]['bg'] = "blue" if self.slLooping else "white" 

#   menu and menu setup for the sl functions
    def slMenuSetup(self):
        self.slLoopSel = [
            [
                tk.Label(self, text="loop start"),
                tk.Label(self, text="loop end"),
                tk.Label(self, text="song length"),
            ],
            [
                tk.Entry(self),
                tk.Entry(self),
                tk.Entry(self),
            ]
        ]
        self.slFileSel = [
            [tk.Label(self, text="file")],
            [tk.Entry(self)],
        ]

        self.slFileSel[1][0].insert(END, SL_DIR)
        
        self.slButtons = [
            [
                tk.Button(self, text="Load",   bg="white", command=self.slLoadSong),
                tk.Button(self, text="Load+",  bg="white", command=self.slLoadAuto),
                tk.Button(self, text="Auto",   bg="white", command=self.slAutoBounds),
                tk.Button(self, text="Update", bg="white", command=self.slManualBounds),
            ],
            [
                tk.Button(self, text="Play",   bg="white", command=lambda: self.slPlay(pressed=True)),
                tk.Button(self, text="Pause",  bg="white", command=self.slPause),
                tk.Button(self, text="Stop",   bg="white", command=self.slStop),
                tk.Button(self, text="Loop",   bg="white", command=self.slToggleLoop),
            ]
        ]

    def slMenu(self, offset=0, padding=8):
        dimCur = [0, offset]

        slLabel = tk.Label(self, text="Sound Looper")
        slLabel.place(
            anchor=N,
            relx=0.5,
            y=dimCur[1],
        )
        dimCur[1] += slLabel.winfo_reqheight()

        dimNew = self.alignedTextPairColumn(self.slFileSel[0], self.slFileSel[1], offset=dimCur[1], width=256, align=128)
        dimCur = self.newBoundsVertical(dimCur, dimNew)

        dimCur[1] += padding
        dimNew = self.centeredButtonRow(self.slButtons[0], offset=dimCur[1])
        dimCur = self.newBoundsVertical(dimCur, dimNew)

        dimCur[1] += padding
        dimNew = self.alignedTextPairColumn(self.slLoopSel[0], self.slLoopSel[1], offset=dimCur[1], align=32)
        dimCur = self.newBoundsVertical(dimCur, dimNew)

        dimCur[1] += padding
        dimNew = self.centeredButtonRow(self.slButtons[1], offset=dimCur[1])
        dimCur = self.newBoundsVertical(dimCur, dimNew)

        dimCur[1] -= offset
        return dimCur 

#   Current implementation has the app run from this script
#   unsure what functionality would cause this to change...
def main():
    UI = UserInterface()
    UI.mainloop()

if __name__ == "__main__":
    main()