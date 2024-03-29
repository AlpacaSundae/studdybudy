import pymusiclooper.core as pm
import sounddevice as sd

class SoundLooperError(Exception):
    pass

class SoundLooper(pm.MusicLooper):
    def __init__(self, filepath, min_duration_multiplier=0.35, trim=True):
        try:
            super().__init__(filepath, min_duration_multiplier, trim)
            self.loopStart = 0
            self.loopEnd = self.mlaudio.length
            self.curFrame = 0
            self.startFrom = 0
            self.looping = False
            self.loopNo = 0
            self.setLoop(self.loopStart, self.loopEnd, self.startFrom)
        except:
            raise SoundLooperError(f"File \"{filepath}\" could not be loaded")

    def getSongName(self):
        return self.mlaudio.filename

    # returns the song length in seconds   
    def getSongLength(self):
        return self.mlaudio.total_duration
    
    def getCurrentTime(self):
        return self.mlaudio.samples_to_seconds(self.curFrame)
    
    # value between 0 and 1 representing the progress through entire song length
    def getPlayPercentage(self):
        return (self.curFrame / self.mlaudio.length)
    
    def setPlayPercentage(self, percent):
        self.curFrame = int(percent * self.mlaudio.length)
        if self.curFrame > self.loopEnd:
            self.curFrame = self.loopEnd

    # returns the loop points [in, out] in (UNITS??)
    def getLooping(self):
        return self.looping
    
    def getLoop(self):
        # check if valid
        if (
            self.loopStart < self.loopEnd
            and self.loopStart >= 0 
            and self.loopEnd <= self.mlaudio.length
        ):
            return [self.loopStart, self.loopEnd]
        # return none if not valid or set
        else:
            return None
        
    def getSampleAsSec(self, no):
        return self.mlaudio.samples_to_seconds(no)

    # automatically determins the loop points
    def autosetLoop(self):
        pair = self.find_loop_pairs()[0]
        self.setLoop(pair.loop_start, pair.loop_end, startFrom=0)

    # used for manually setting the loop points
    # startFrom variable defines where the song should start playback when played
    def setLoop(self, loopStart, loopEnd, startFrom=0):
        self.loopStart = loopStart
        self.loopEnd = loopEnd
        self.curFrame = startFrom
        self.startFrom = startFrom
        self.setLooping(loop=True)
        self.loopNo = 0

    def setLooping(self, loop=True):
        self.looping = True

    def resetPlayback(self):
        self.curFrame = self.startFrom

    def startPlayback(self):
        # Function is entirely copied from "playback.py" of https://github.com/arkrow/PyMusicLooper just with variables renamed to follow my naming...
        def sdCallback(outdata, frames, time, status):
            chunksize = min(len(self.mlaudio.playback_audio) - self.curFrame, frames)

            if self.looping and self.curFrame + frames > self.loopEnd:
                loopFrameIdx = self.loopEnd - self.curFrame                 # frame idx for outdata after which the loop will restart from loopStart
                remainingFrames = frames - (self.loopEnd - self.curFrame)   # space left for frames of the next loop 
                nextFrameIdx = self.loopStart + remainingFrames             # final frame idx to include after loopStart i.e., the next value of curFrame

                outdata[:loopFrameIdx] = self.mlaudio.playback_audio[self.curFrame : self.loopEnd]
                outdata[loopFrameIdx : frames] = self.mlaudio.playback_audio[self.loopStart : nextFrameIdx]
                self.curFrame = nextFrameIdx
                self.loopNo += 1
            else:
                outdata[:chunksize] = self.mlaudio.playback_audio[self.curFrame : self.curFrame + chunksize]
                self.curFrame += frames
                if chunksize < frames:
                        outdata[chunksize:] = 0
                        raise sd.CallbackStop()
            
        self.stream = sd.OutputStream(samplerate=self.mlaudio.rate, callback=sdCallback, channels=self.mlaudio.n_channels)
        self.stream.start()

    def stopPlayback(self):
        if hasattr(self, "stream"):
            self.stream.stop()
        else:
            raise SoundLooperError("No playback stream has been created yet. Have you started playback before?")

def main():
    file = "D:\\Desktop\\studdybudy\\media\\looper\\de_spicy.mp3"
    slPlayer = SoundLooper(file)
    slPlayer.autosetLoop()

    while (True):
        slPlayer.startPlayback()
        input()
        slPlayer.stopPlayback()
        input()
    

if __name__ == "__main__":
    main()