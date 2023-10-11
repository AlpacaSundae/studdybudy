from SoundRandomiser import *
from SoundLooper import *
pygame.init()

import os.path
import customtkinter as ctk
from threading import Thread

class UserInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.mainMenu()
        self.sr = SoundRandomiserUI(self) # sr = SoundRandomiser
        self.sr.pack(anchor="n", side=ctk.TOP)
        self.sl = SoundLooperUI(self) # sr = SoundRandomiser
        self.sl.pack(anchor="n", side=ctk.TOP)

    def mainMenu(self):
        self.title("studdy budy 2.0")
        #self.geometry("400x400")
        self.status()

    def status(self):
        self.status = ctk.CTkLabel(self, width=32, justify=ctk.LEFT, text="welcome! "*3)
        self.status.pack(anchor="sw", side=ctk.BOTTOM)

    # TODO: make this function not resize the window if the text is too big..
    #       but also allow for resizing/scrolling to view long messages
    def statusMessage(self, msg):
        print(msg)
        self.status.configure(text=msg)

#
#   SoundRandomiser menu functions 
#
class SoundRandomiserUI(ctk.CTkFrame):
    def __init__(self, parent : UserInterface):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        self.srPlayer = SoundRandomiser(prob=0.0625)
        # interval = ms before function should be called again by tk's mainloop
        self.srInterval = 50
        # change if the randomiser is on or not
        self.srRun = False
        self.srMenu()

    def srToggle(self, run=False):
        if run:
            if not self.srRun:
                self.parent.statusMessage("starting SoundRandomiser playback loop")
                self.srRun = True
                self.srPlay()
            else:
                self.parent.statusMessage("SoundRandomiser already running!")
        elif self.srRun:
            self.parent.statusMessage("stopping SoundRandomiser playback loop")
            self.srRun = False
        else:
            self.parent.statusMessage("SoundRandomiser isn't running...")

    # repeatedly rolls for a sfx chance given srRun is true
    def srPlay(self):
        if self.srRun:
            self.srPlayer.roll()
            self.after(self.srInterval, self.srPlay)

    def srUpdateProb(self):
        self.srProbability["sProb"].set(f"{100*self.srPlayer.prob:3.2f}%")
        self.srProbability["sFreq"].set(f"{self.srInterval:.0f}ms")
        self.srProbability["sTrpt"].set(f"{self.srInterval/self.srPlayer.prob:.0f}ms per sfx")
        self.srProbability["probSlider"].set(self.srPlayer.prob)
        self.srProbability["freqSlider"].set(self.srInterval)

    def probSlidier(self, prob):
        self.srPlayer.setProbability(prob)
        self.srUpdateProb()

    def freqSlidier(self, val):
        self.srInterval = int(val)
        self.srUpdateProb()

    def srMenu(self):
        ctk.CTkLabel(self, text="Sound Randomiser").grid(row=0, column=0, columnspan=2)
        ctk.CTkButton(self, text="Start", width=96, command=lambda: self.srToggle(True)).grid(row=1, column=0, padx=8)
        ctk.CTkButton(self, text="Stop" , width=96, command=lambda: self.srToggle(False)).grid(row=1, column=1, padx=8)

        self.srProbability = {
            "sProb" : ctk.StringVar(),
            "sFreq" : ctk.StringVar(),
            "sTrpt" : ctk.StringVar(),
            "probSlider" : ctk.CTkSlider(self, from_=0.0005, to=1, number_of_steps=1999, command=self.probSlidier),
            "freqSlider" : ctk.CTkSlider(self, from_=10, to=1000, number_of_steps=990, command=self.freqSlidier),
        }
        self.srUpdateProb()
        
        ctk.CTkLabel(self, text="probability: ").grid(row=2, column=0, sticky="e")
        ctk.CTkLabel(self, text=  "frequency: ").grid(row=4, column=0, sticky="e")
        ctk.CTkLabel(self, text= "throughput: ").grid(row=6, column=0, sticky="e")
        ctk.CTkLabel(self, textvariable=self.srProbability["sProb"]).grid(row=2, column=1, sticky="w")
        ctk.CTkLabel(self, textvariable=self.srProbability["sFreq"]).grid(row=4, column=1, sticky="w")
        ctk.CTkLabel(self, textvariable=self.srProbability["sTrpt"]).grid(row=6, column=1, sticky="w")
        self.srProbability["probSlider"].grid(row=3, column=0, columnspan=2)
        self.srProbability["freqSlider"].grid(row=5, column=0, columnspan=2)

class SoundLooperUI(ctk.CTkFrame):
    ERROR_NO_PLAYER = "No slPlayer object found"
    DEFAULT_ROOT_DIR = os.path.abspath("./media/looper")
    THREAD_CHECK_INTERVAL = 1000 #msec
    THREAD_TIMEOUT = 0.25 #sec

    def __init__(self, parent : UserInterface):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        self.slPlayer = None
        self.initSettings()
        self.slMenu()

    def loadSong(self):
        if self.slPlayer is not None:
            try:
                self.slPlayer.stopPlayback()
            except:
                pass # TODO: make .stopPlayback() check if it was actually playing first
        try:
            self.parent.statusMessage("slPlayer: loading...")
            # TODO: thread this as well
            self.slPlayer = SoundLooper(filepath=os.path.join(self.slSettings["root_dir"], self.slSettings["filename"].get()))
            self.parent.statusMessage("slPlayer: loaded!")
        except SoundLooperError as e:
            self.parent.statusMessage(f"Error creating slPlayer: {e}")

    def autosetLoop(self):
        if self.slPlayer:
            self.parent.statusMessage("slPlayer: finding loop points...")
            t = Thread(target=self.slPlayer.autosetLoop)
            t.start()
            self.after(self.THREAD_CHECK_INTERVAL, self.autosetLoopCheck, t, 0)
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)

    def autosetLoopCheck(self, t : Thread, count=0):
        t.join(timeout=self.THREAD_TIMEOUT)
        if (t.is_alive()):
            count += 1
            self.parent.statusMessage(f"slPlayer: finding loop points... [{count}]")
            self.after(self.THREAD_CHECK_INTERVAL, self.autosetLoopCheck, t, count)
        else:
            if (self.slPlayer.getLoop()):
                self.parent.statusMessage("slPlayer: loop points are go")
            else:
                self.parent.statusMessage("slPlayer: failed to find loop points ):")

    def play(self):
        if self.slPlayer:
            self.slPlayer.startPlayback()
            self.parent.statusMessage("slPlayer: playing")
        else:
            self.parent.statusMessage(f"{self.ERROR_NO_PLAYER}: have you loaded a song?")

    def pause(self):
        if self.slPlayer:
            self.slPlayer.stopPlayback()
            self.parent.statusMessage("slPlayer: paused")
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)

    def stop(self):
        if self.slPlayer:
            self.slPlayer.stopPlayback()
            self.parent.statusMessage("slPlayer: stopping...")
            self.slPlayer.resetPlayback()
            self.parent.statusMessage("slPlayer: stopped")
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)

    def initSettings(self):
        self.slSettings = {
            "root_dir" : self.DEFAULT_ROOT_DIR,
            "filename" : ctk.StringVar(),
        }

    def slMenu(self):
        ctk.CTkLabel(self, text="Sound Looper").grid(row=0, column=0, columnspan=3)
        ctk.CTkButton(self, text="Play", width=96, command=self.play).grid(row=1, column=0, padx=8)
        ctk.CTkButton(self, text="Pause", width=96, command=self.pause).grid(row=1, column=1, padx=8)
        ctk.CTkButton(self, text="Stop", width=96, command=self.stop).grid(row=1, column=2, padx=8)

        ctk.CTkLabel(self, text="filename:").grid(row=2, column=0)
        ctk.CTkEntry(self, textvariable=self.slSettings["filename"]).grid(row=2, column=1, columnspan=2, pady=8)
        ctk.CTkButton(self, text="load", width=96, command=self.loadSong).grid(row=3, column=0, padx=8)
        ctk.CTkButton(self, text="autoset loop", width=96, command=self.autosetLoop).grid(row=3, column=1, padx=8)

def main():
    UI = UserInterface()
    UI.mainloop()     
    
if __name__ == "__main__":
    main()