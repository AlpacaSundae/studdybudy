import pymusiclooper.core as pm

class SoundLooperError(Exception):
    pass

class SoundLooper(pm.MusicLooper):
    def __init__(self, filepath, min_duration_multiplier=0.35, trim=True):
        try:
            super().__init__(filepath, min_duration_multiplier, trim)
        except FileNotFoundError:
            raise SoundLooperError(f"File \"{filepath}\" could not be loaded")

    # returns the song length in (UNITS??)   
    def getSongLength(self):
        pass

    # returns the loop points [in, out] in (UNITS??)
    def getLooping(self):
        pass

    # automatically determins the loop points
    def autosetLooping(self):
        pass

    # used for manually setting the loop points
    # startFrom variable defines where the song should start playback when played
    def setLooping(self, loopIn, loopEnd, startFrom=0):
        pass

def main():
    file = "D:\\Desktop\\studdybudy\\media\\looper\\de_spicy.mp3"
    slPlayer = SoundLooper(file)

    try:
        slPlayer.autosetLooping()
    except SoundLooperError as e:
        slPlayer.setLooping(1000, 1200, 500)

if __name__ == "__main__":
    main()