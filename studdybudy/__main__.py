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
        # first menu: sr = SoundRandomiser
        self.sr = SoundRandomiserUI(self)
        self.sr.pack(anchor="n", side=ctk.TOP, pady=16, padx=16)
        # second menu: sl = SoundLooper
        self.sl = SoundLooperUI(self)
        self.sl.pack(anchor="n", side=ctk.TOP, pady=16, padx=16)

        # Set the window minimum size to the initial window size
        self.update()
        self.after_idle(lambda: self.minsize(self.winfo_width(), self.winfo_height()))

    # properties to set up the main window
    def mainMenu(self):
        self.title("studdy budy 2.0")
        #self.geometry("400x400")
        self.status()

    # status bar used to display messages at the bottom of window
    def status(self):
        self.status = ctk.CTkLabel(self, width=32, justify=ctk.LEFT, text="welcome! "*3)
        self.status.pack(anchor="sw", side=ctk.BOTTOM)

    def statusMessage(self, msg, info=None):
        print(msg)
        if info:
            print(f"-> {info}")
        self.status.configure(text=msg)
        # TODO: make this function not resize the window if the text is too big..
        #       but also allow for resizing/scrolling to view long messages

#
#   SoundRandomiser functions
#     -- This interfaces the SoundRandomiser script with a ctk frame for the main window
#     -- functionality exposed:
#               start/stop randomiser, 
#               adjust frequency and probability of playback
#
class SoundRandomiserUI(ctk.CTkFrame):
    def __init__(self, parent : UserInterface):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        try:
            self.srPlayer = SoundRandomiser(prob=0.0625)
        except SoundRandomiserError as e:
            self.srPlayer = None
            self.parent.statusMessage("Unable to create srPLayer", info=e)
        self.srRootDir = ctk.StringVar(value=self.srPlayer.getRootDir())
        # interval = ms before function should be called again by tk's mainloop
        self.srInterval = 50
        # defines if the randomiser is running or not
        self.srRun = False
        self.srMenu()

    def srToggle(self, run=False):
        if run:
            if self.srPlayer is None:
                self.parent.statusMessage("SoundRandomiser not initialised...")
            elif not self.srRun:
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

    def srLoadDir(self):
        self.parent.statusMessage("Loading SoundRandomiser directory", info=self.srRootDir.get())
        try:
            self.srPlayer.sfxLoadDir(self.srRootDir.get(), init=False)
            self.srDirSelector["dirBox"].configure(values=self.srPlayer.getSubDirListAll())
            self.parent.statusMessage("SoundRandomiser directory loaded!")
        except SoundRandomiserError as e:
            self.parent.statusMessage("SoundRandomiser unable to load directory", info=e)

    # repeatedly rolls for a sfx chance given srRun is true
    def srPlay(self):
        if self.srRun:
            self.srPlayer.roll()
            self.after(self.srInterval, self.srPlay)

    #
    # Sliders
    #   -- Adjust the probability and frequency of rolls 
    #
    def srUpdateProb(self):
        if self.srPlayer:
            self.srProbability["sProb"].set(f"{100*self.srPlayer.prob:3.2f}%")
            self.srProbability["sFreq"].set(f"{self.srInterval:.0f}ms")
            # sTrpt : throughput is estimated based on the settings for now
            # TODO: track the actual throughpout and display that instead 
            self.srProbability["sTrpt"].set(f"{self.srInterval/self.srPlayer.prob:.0f}ms per sfx")
            self.srProbability["probSlider"].set(self.srPlayer.prob)
            self.srProbability["freqSlider"].set(self.srInterval)
        else:
            self.parent.statusMessage("SoundRandomiser not initialised...")

    def probSlidier(self, prob):
        if self.srPlayer:
            self.srPlayer.setProbability(prob)
        else:
            self.parent.statusMessage("SoundRandomiser not initialised...")
        self.srUpdateProb()

    def freqSlidier(self, val):
        self.srInterval = int(val)
        self.srUpdateProb()

    def selectDirectory(self, dirStr):
        if self.srPlayer.getSubDirStatus(dirStr):
            self.srDirSelector["status"].set(1)
        else:   
            self.srDirSelector["status"].set(0)

    def toggleDirectory(self):
        try:
            dirStr = self.srDirSelector["curDir"].get()
            if self.srDirSelector["status"].get() == 1:
                self.srPlayer.enableSubDir(dirStr)
                self.parent.statusMessage(f"Enabled randomiser on: {dirStr.split(os.sep)[-1]}")
            else:
                self.srPlayer.disableSubDir(dirStr)
                self.parent.statusMessage(f"Disabled randomiser on: {dirStr.split(os.sep)[-1]}")
        except SoundRandomiserError as e:
            self.parent.statusMessage("SoundRandomiser unable to toggle directory", info=e)

    def soloDirectory(self):
        try:
            dirStr = self.srDirSelector["curDir"].get()
            self.srPlayer.setSubDirList([dirStr])
            self.srDirSelector["status"].set(1)
            self.parent.statusMessage(f"Randomiser solo on: {dirStr.split(os.sep)[-1]}")
        except SoundRandomiserError as e:
            self.parent.statusMessage("SoundRandomiser unable to toggle directory", info=e)

    # 
    # SoundRandomiser menu setup function
    #   -- very simple
    #
    def srMenu(self):
        row = 0
        ctk.CTkLabel(self, text="Sound Randomiser").grid(row=row, column=0, columnspan=3)
        row += 1
        ctk.CTkButton(self, text="Start", width=96, command=lambda: self.srToggle(True)).grid(row=row, column=0, padx=8)
        ctk.CTkButton(self, text="Stop" , width=96, command=lambda: self.srToggle(False)).grid(row=row, column=1, padx=8)
        ctk.CTkButton(self, text="Load" , width=96, command=self.srLoadDir).grid(row=row, column=2, padx=8)

        self.srProbability = {
            "sProb" : ctk.StringVar(),
            "sFreq" : ctk.StringVar(),
            "sTrpt" : ctk.StringVar(),
            "probSlider" : ctk.CTkSlider(self, from_=0.0005, to=1, number_of_steps=1999, command=self.probSlidier),
            "freqSlider" : ctk.CTkSlider(self, from_=10, to=1000, number_of_steps=990, command=self.freqSlidier),
        }
        self.srUpdateProb()
        
        row += 1
        ctk.CTkLabel(self, text="sfx directory: ").grid(row=row, column=0)
        ctk.CTkEntry(self, textvariable=self.srRootDir).grid(row=row, column=1, columnspan=2, pady=8, sticky="ew")

        row += 1
        self.srDirSelector = {
            "curDir" : ctk.StringVar(),
            "status" : ctk.Variable(),
            "dirBox" : ctk.CTkComboBox(self, justify="right", values=self.srPlayer.getSubDirListAll(), command=self.selectDirectory),
        }
        ctk.CTkLabel(self, text= "sub-directory:").grid(row=row, column=0)
        self.srDirSelector["dirBox"].configure(variable=self.srDirSelector["curDir"])
        self.srDirSelector["dirBox"].grid(row=row, column=1, columnspan=2, pady=8, sticky="ew")
        row += 1
        ctk.CTkButton(self, text="Solo", width=96, command=self.soloDirectory).grid(row=row, column=2, padx=8)
        ctk.CTkCheckBox(self, text="Enabled?", onvalue=1, offvalue=0, command=self.toggleDirectory, variable=self.srDirSelector["status"]).grid(row=row, column=1)

        row += 1
        ctk.CTkLabel(self, text=" ", height=0).grid(row=row, column=0)
        row += 1
        ctk.CTkLabel(self, text="probability: ", height=0).grid(row=row, column=0, sticky="s")
        ctk.CTkLabel(self, textvariable=self.srProbability["sProb"], height=0).grid(row=row+1, column=0, sticky="ne", ipadx=8)
        self.srProbability["probSlider"].grid(row=row, column=1, columnspan=2, rowspan=2)
        row += 2

        ctk.CTkLabel(self, text=  "frequency: ", height=0).grid(row=row, column=0, sticky="s")
        ctk.CTkLabel(self, textvariable=self.srProbability["sFreq"], height=0).grid(row=row+1, column=0, sticky="ne", ipadx=8)
        self.srProbability["freqSlider"].grid(row=row, column=1, columnspan=2, rowspan=2)
        row += 2

        ctk.CTkLabel(self, text= "throughput: ").grid(row=row, column=0)
        ctk.CTkLabel(self, textvariable=self.srProbability["sTrpt"]).grid(row=row, column=1, columnspan=2, sticky="w", ipadx=8)

#
#   SoundLooper functions
#     -- Similarly, this interfaces the SoundLooper script with a ctk frame for the main window
#     -- functionality exposed:
#               load song, auto-set loop points
#               play/pause/stop playback
#               progress slider and seek ability
#               set directory and audio file
#     -- TODO
#               allow for manually set loop points
#
class SoundLooperUI(ctk.CTkFrame):
    SL_ERROR = "SoundLooper object threw an error"
    ERROR_NO_PLAYER = "No slPlayer object found"
    DEFAULT_ROOT_DIR = os.path.abspath("./media/looper")
    THREAD_TIMEOUT = 0.05 #sec
    THREAD_CHECK_INTERVAL = 950 #msec
    PROGRESS_UPDATE_INTERVAL = 1000

    def __init__(self, parent : UserInterface):
        ctk.CTkFrame.__init__(self, parent)
        self.parent = parent
        self.slPlayer = None
        self.slMenu()

    def loadSong(self):
        if self.slPlayer is not None:
            try:
                self.slPlayer.stopPlayback()
            except:
                pass # TODO: make .stopPlayback() check if it was actually playing first
        try:
            self.parent.statusMessage("slPlayer: loading...")
            # TODO: thread this as well to stop UI freeze on load
            self.slPlayer = SoundLooper(filepath=os.path.join(self.stringVars["root_dir"].get(), self.stringVars["filename"].get()))
            self.parent.statusMessage("slPlayer: loaded!")
        except SoundLooperError as e:
            self.parent.statusMessage(f"Error creating slPlayer", info=e)

        self.setTimeStrings()

    def setTimeStrings(self):
        if self.slPlayer is None:
            self.stringVars["loopStr"].set("0:00 - 0:00")
            self.stringVars["songLength"].set("0:00 / 0:00")
        else:
            loop = self.slPlayer.getLoop()
            lenSec = self.slPlayer.getSongLength()
            curSec = self.slPlayer.getCurrentTime()

            if loop is not None:
                loopA = self.slPlayer.getSampleAsSec(loop[0])
                loopB = self.slPlayer.getSampleAsSec(loop[1])
                self.stringVars["loopStr"].set(f"{loopA // 60:02.0f}:{loopA % 60:02.0f} - {loopB // 60:02.0f}:{loopB % 60:02.0f}")
            self.stringVars["songLength"].set(f"{curSec // 60:02.0f}:{curSec % 60:02.0f} / {lenSec // 60:02.0f}:{lenSec % 60:02.0f}")

    def manualsetLoop(self):
        if not self.slPlayer:
            self.loadSong()
        if self.slPlayer:
            # spawn a window with on the left the current loop start, loop end, song length (in frames)
            #                     on the right an entry for loop start and loop end
            # a button to test the loop point (play from 5s before to 5s after loop point)
            # a buttons to confirm or cancel
            pass # TODO: all of the above lmao
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)

    # this uses pymusiclooper's functionality to automatically select points to loop between
    def autosetLoop(self):
        if not self.slPlayer:
            self.loadSong()
        if self.slPlayer:
            self.parent.statusMessage("slPlayer: finding loop points...")
            t = Thread(target=self.slPlayer.autosetLoop)
            t.start()
            self.after(self.THREAD_CHECK_INTERVAL, self.autosetLoopCheck, t, 0)
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)

    def autosetLoopCheck(self, t : Thread, count=0):
        # periodically tries to rejoin the thread with timeout to minimise UI freeze
        # when the thread is no longer alive, loop points have been set
        t.join(timeout=self.THREAD_TIMEOUT)
        if (t.is_alive()):
            count += 1
            self.parent.statusMessage(f"slPlayer: finding loop points... [{count}]")
            self.after(self.THREAD_CHECK_INTERVAL, self.autosetLoopCheck, t, count)
        else:
            if (self.slPlayer.getLoop()):
                self.setTimeStrings()
                self.parent.statusMessage("slPlayer: loop points are go")
            else:
                self.parent.statusMessage("slPlayer: failed to find loop points ):")

    # user can seek through the song using this function
    def progressBarManual(self, value):
        if self.slPlayer:
            self.slPlayer.setPlayPercentage(value)
            self.setTimeStrings()

    # this updates the position of the progress bar each [defined interval]
    # needs to be restarted whenever playback is stopped
    def progressBarUpdate(self):
        if self.playing:
            self.playProgress.set(self.slPlayer.getPlayPercentage())
            self.setTimeStrings()
            self.after(self.PROGRESS_UPDATE_INTERVAL, self.progressBarUpdate)

    def play(self):
        if self.playing:
            self.parent.statusMessage("slPlayer: already playing")
        elif self.slPlayer:
            self.slPlayer.startPlayback()
            self.playing = True
            self.progressBarUpdate()
            self.parent.statusMessage("slPlayer: playing")
        else:
            self.parent.statusMessage(f"{self.ERROR_NO_PLAYER}: have you loaded a song?")

    def pause(self):
        if not self.playing:
            self.parent.statusMessage("slPlayer: already paused")
        elif self.slPlayer:
            try:
                self.slPlayer.stopPlayback()
                self.parent.statusMessage("slPlayer: paused")
            except SoundLooperError as e:
                self.parent.statusMessage(self.SL_ERROR, e)
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)
        self.playing = False

    def stop(self):
        if self.slPlayer:
            try:
                if self.playing:
                    self.parent.statusMessage("slPlayer: stopping...")
                    self.slPlayer.stopPlayback()
                self.slPlayer.resetPlayback()
                self.parent.statusMessage("slPlayer: stopped")
            except SoundLooperError as e:
                self.parent.statusMessage(self.SL_ERROR, e)
        else:
            self.parent.statusMessage(self.ERROR_NO_PLAYER)        
        # reset the slider and playback text
        self.playProgress.set(0.0)
        self.setTimeStrings()
        self.playing = False

    def slMenu(self):
        self.stringVars = {
            "root_dir"      : ctk.StringVar(value=self.DEFAULT_ROOT_DIR),
            "filename"      : ctk.StringVar(value="barracks_settlement.opus"),
            "loopStr"       : ctk.StringVar(value="0:00 - 0:00"),
            "songLength"    : ctk.StringVar(value="0:00 / 0:00"),
            "curProgress"   : ctk.StringVar(),
        }
        self.playProgress = ctk.DoubleVar(value=0.0)
        self.playing = False

        row = 0
        
        ctk.CTkLabel(self, text="Sound Looper").grid(row=row, column=0, columnspan=3)
        row += 1
        
        ctk.CTkButton(self, text="Play", width=96, command=self.play).grid(row=row, column=0, padx=8)
        ctk.CTkButton(self, text="Pause", width=96, command=self.pause).grid(row=row, column=1, padx=8)
        ctk.CTkButton(self, text="Stop", width=96, command=self.stop).grid(row=row, column=2, padx=8)
        row += 1
        
        ctk.CTkLabel(self, text="directory:").grid(row=row, column=0)
        ctk.CTkEntry(self, textvariable=self.stringVars["root_dir"]).grid(row=row, column=1, columnspan=2, pady=8, sticky="ew")
        row += 1
        
        ctk.CTkLabel(self, text="filename:").grid(row=row, column=0)
        ctk.CTkEntry(self, textvariable=self.stringVars["filename"]).grid(row=row, column=1, columnspan=2, pady=8, sticky="ew")
        row += 1
        
        ctk.CTkButton(self, text="load", width=96, command=self.loadSong).grid(row=row, column=0, padx=8)
        ctk.CTkButton(self, text="auto-set loop", width=96, command=self.autosetLoop).grid(row=row, column=1, padx=8)
        ctk.CTkButton(self, text="manual-set loop", width=96, command=self.manualsetLoop, state=ctk.DISABLED).grid(row=row, column=2, padx=8)
        row += 1

        ctk.CTkLabel(self, text="loop", anchor="se").grid(row=row, column=0, columnspan=2, sticky="s")
        ctk.CTkLabel(self, text="runtime", anchor="sw").grid(row=row, column=1, columnspan=2, sticky="s")
        row += 1

        ctk.CTkLabel(self, textvariable=self.stringVars["loopStr"], anchor="ne").grid(row=row, column=0, columnspan=2, sticky="n")
        ctk.CTkLabel(self, textvariable=self.stringVars["songLength"], anchor="nw").grid(row=row, column=1, columnspan=2, sticky="n")
        row += 1

        ctk.CTkSlider(self, from_=0, to=1, variable=self.playProgress, command=self.progressBarManual).grid(row=row, column=0, columnspan=3, sticky="ew")
        row += 1

def main():
    UI = UserInterface()
    UI.mainloop()     
    
if __name__ == "__main__":
    main()