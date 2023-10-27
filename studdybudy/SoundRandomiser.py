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
        self.root_dir = os.path.normpath(sfx_dir)
        self.sfxLoadDir(self.root_dir)
        self.setProbability(prob)
        self.stop = False

    # loads any wav files in the directory provided
    # checks subfolders to allow the user to sort samples
    # each subdirectory is stored as a new list within the sfx_store dict
    def sfxLoadDir(self, sfx_dir, init = True):
            if (not os.path.isdir(sfx_dir)):
                raise SoundRandomiserError(f"\'{sfx_dir}\' is not a valid directory")
            
            if (init):
                self.sfx_store = {}
                self.sfx_alt_store = {}

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

            if (len(self.sfx_store) == 0):
                raise SoundRandomiserError(f"no .wav files could be loaded from: \'{sfx_dir}\'")

    def setProbability(self, prob):
        if (prob >= 0 and prob <= 1):
            self.prob = prob
        else:
            raise SoundRandomiserError(f"Probablitiy must be in range [0.0, 1.0], given: {prob}")

    def playRandom(self):
        random.choice(random.choice(list(self.sfx_store.values()))).play()

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