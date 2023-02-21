import pygame
import pymusiclooper.core as pm

import librosa

#
#   Shoutout to https://github.com/arkrow/PyMusicLooper for creating an automatic
#   way for initialising loop points for this project !!
#
#   This extends the afforementioned package by adding in methods to track and
#   playback the looped music via continuous calls to play_looping_update()
#   this allows integration and control alongside other codes
#

class SoundLooperFinished(Exception):
    pass

class SoundLooperError(Exception):
    pass

class SoundLooper(pm.MusicLooper):
    def get_looping(self):
        return [self.loop_start, self.loop_end]

    def autoset_looping(self):
        try:
            pairs = self.find_loop_pairs()
            self.set_looping(pairs[0]["loop_start"], pairs[0]["loop_end"])
        except Exception:
            raise SoundLooperError("Could not automatically determine loop region")
    
    def set_looping(self, loop_start, loop_end, start_from=0):
        self.loop_start = loop_start
        self.loop_end = loop_end
        self.start_from = start_from

        try:
            from mpg123 import ENC_FLOAT_32, Out123
            self.out = Out123()
            self.out.start(self.rate, self.channels, ENC_FLOAT_32)
        except Exception as e:
            raise SoundLooperError('An issue related to the mpg123 library for playback has occured.')

        self.playback_frames = librosa.util.frame(self.playback_audio.flatten(order="F"), frame_length=2048, hop_length=512)
        self.loop_start = self.loop_start * self.channels
        self.loop_end = self.loop_end * self.channels
        self.start_from = self.start_from * self.channels

        self.playidx = self.start_from
        self.idx_end = self.playback_frames.shape[-1]

    def play_looping_update(self, contLoop=True):
        self.out.play(self.playback_frames[..., self.playidx])
        self.playidx += 1
        if contLoop:
            if self.playidx >= self.loop_end or self.playidx >= self.idx_end:
                self.playidx = self.loop_start
        else:
            if (self.playidx >= self.idx_end):
                raise SoundLooperFinished
 



def main():
    file = "/hdd/Saving Stuff/Music/NOFX/Compilations/2002 - 45 Or 46 Songs That Weren't Good Enough To Go On Our Other Records/1-12 See Her Pee.mp3"
    loaded = SoundLooper(file)

    try:
        loaded.autoset_looping()
    except SoundLooperError as e:
        loaded.set_looping(2000, 2300, 1500)
        
    print(loaded.get_looping())

    while (loop(loaded)):
        pass

def loop(loaded):
    try:
        loaded.play_looping_update(False)
        return True
    except SoundLooperFinished:
        return False

if __name__ == "__main__":
    main()