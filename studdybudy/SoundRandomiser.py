import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

class SoundRandomiserError(Exception):
    pass

# A very simple script for playing back random sound effects randomly
# Sound effects are loaded in from a directory (and its subs) and played back with pygame
class SoundRandomiser():
    def __init__(self, sfx_dir = "./media/randomiser", prob = 0.0000001):
        self.sfx_store = {}
        self.sfx_enabled = set()
        self.root_dir = os.path.abspath(sfx_dir)
        self.sfxLoadDir(self.root_dir)
        self.setProbability(prob)

    # loads any wav files in the directory provided
    # checks subfolders to allow the user to sort samples
    # each subdirectory is stored as a new list within the sfx_store dict
    def sfxLoadDir(self, sfx_dir, init = True):
            if (not os.path.isdir(sfx_dir)):
                raise SoundRandomiserError(f"\'{sfx_dir}\' is not a valid directory")
            
            if (init):
                self.sfx_store = {}
                self.sfx_enabled = set()

            for root, dirs, files in os.walk(sfx_dir):
                # for each subdirectory with files we will create a list of pygame sounds
                temp_store = []
                for filename in files:
                    if filename.lower().endswith(".wav"):
                        try:
                            temp_store.append(pygame.mixer.Sound(os.path.join(root, filename)))
                        except pygame.error as e:
                            print(f"Error loading file: {os.path.join(root, filename)}") # print info for now,, might change to raise error later
                
                # and we add it to the sfx dict only if a sound file was found and loaded
                if (len(temp_store) != 0):
                    self.sfx_store[root] = temp_store
                    if root not in self.sfx_enabled:
                        self.sfx_enabled.add(root)

            if (len(self.sfx_store) == 0):
                raise SoundRandomiserError(f"no .wav files could be loaded from: \'{sfx_dir}\'")

    def setProbability(self, prob):
        if (prob >= 0 and prob <= 1):
            self.prob = prob
        else:
            raise SoundRandomiserError(f"Probablitiy must be in range [0.0, 1.0], given: {prob}")

    def getRootDir(self):
        return self.root_dir

    # returns a list of the subdirectories with loaded songs, each entry being an absolute path string
    def getSubDirListAll(self):
        return list(self.sfx_store.keys())
    
    # returns true if the directory is enabled
    def getSubDirStatus(self, dir_str):
        return (dir_str in self.sfx_enabled)

    # adds the input string to self.sfx_enabled if it is found as a key in the sfx dictionary
    def enableSubDir(self, dir_str : str):
        if dir_str in self.sfx_store:
            if dir_str not in self.sfx_enabled:
                self.sfx_enabled.add(dir_str)
            else:
                print(f"{dir_str} is already enabled")
        else:
            raise SoundRandomiserError(f"Could not enable sub directory which has no songs loaded: {dir_str}")
        
    # removes the input string to self.sfx_enabled if it is found as a key in the sfx dictionary
    def disableSubDir(self, dir_str : str ):
        if dir_str in self.sfx_store:
            if dir_str in self.sfx_enabled:
                self.sfx_enabled.remove(dir_str)
            else:
                print(f"{dir_str} is already disabled")
        else:
            raise SoundRandomiserError(f"Could not disable sub directory which has no songs loaded: {dir_str}")
        
    # this is for setting multiple subdirectories
    # uses input as a list of the sub directores to be enabled
    def setSubDirList(self, dir_strs : list[str]):
        self.sfx_enabled = set()
        for cur_str in dir_strs:
            self.enableSubDir(cur_str)

    def playRandom(self):
        if not self.sfx_enabled:
            print("No sfx to randomise...")
        else:
            random.choice(self.sfx_store[random.choice(list(self.sfx_enabled))]).play()

    def roll(self):
        result = random.random()
        if (result < self.prob):
            self.playRandom()

def main():
    pygame.init()
    sfx=SoundRandomiser()
    print("here we go!")
    try:
        while(True):
            sfx.roll()
    except KeyboardInterrupt:
        print(" that's enough of that...")

if __name__ == "__main__":
    main()