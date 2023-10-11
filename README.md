Requires poetry

To install dependencies: 'poetry install'
To run: 'poetry run python studdybudy'

# SoundRandomiser functionality
randomly decides to play a random sound effect
place sfx to loop over in the folder './media/randomiser' (subdirectories are ok!)
these must be formatted as ".wav"
(sfx must be added to the folder before program launch)

* probablity is the chance that a sound will be played, then it is an equal choice between all sfx loaded from the sfx dir
* frequency is how much time will pass between each roll (just ignore that it actually describes the period)

# SoundLooper functionality
load in a song and endlessly loop it!
over here, we use the './media/looper' folder for songs (then you can choose the song by typing just the filename into the program's textbox)
implements https://github.com/arkrow/PyMusicLooper to automagically select ideal points of the song to loop between,,,
format is not as strict here

* type filename
* press load, wait for a sliver of time
* press autoset loop, wait many slivers of time
* now you can use play/pause/stop

# To do:
SR
* allow reloading sfx dir with program open
* implement a playback toggle of the loaded sub directories

SL
* browse/list files in the directory
* allow manual loop point selection
* cache previous loop points for faster song loading

idks
* can I volume controls?? apparently not for sounddevice specifically, so you need to use volume mixer, but maybe I can at some point set the volume mixer from within python
