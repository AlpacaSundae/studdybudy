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
        self.sfxLoad(sfx_dir)
        self.setProbability(prob)
        self.stop = False

    # loads any wav files in the directory provided
    # checks subfolders to allow the user to sort samples
    def sfxLoad(self, sfx_dir, init = True):
        try:
            if (not os.path.isdir(sfx_dir)):
                raise SoundRandomiserError(f"\'{sfx_dir}\' is not a valid directory")

            # this allows reruns for adding dirs without clearing previous loading
            if (init):
                self.sfx_store = []
            
            for root, dirs, files in os.walk(sfx_dir):
                for filename in files:
                    if filename.endswith(".wav"):
                        self.sfx_store.append(pygame.mixer.Sound(os.path.join(root, filename)))

            # len 0 means no wav files ever load
            # only important for functionality on the first dir load
            if (len(self.sfx_store) == 0):
                raise SoundRandomiserError(f"\'{sfx_dir}\' contains no .wav files")

        # must run pygame.init() beforehand
        except pygame.error as e:
            raise SoundRandomiserError("pygame not initialised")

    def setProbability(self, prob):
        if (prob >= 0 and prob <= 1):
            self.prob = prob
        else:
            raise SoundRandomiserError(f"Probablitiy must be in range [0.0, 1.0], given: {prob}")

    def playRandom(self):
        random.choice(self.sfx_store).play()

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