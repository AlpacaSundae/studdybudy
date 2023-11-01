Requires poetry `https://python-poetry.org/docs/#installing-with-the-official-installer`

# Usage

## Windows Users

* After installing poetry, ensure it is available in your PATH (verify with `poetry about`)
* Launch "install.bat" to install dependencies
* Run with the newly created shortcut, "studdybudy" 
  * You can always just run with "run.bat" if desired, but the shortcut will hide the command window

If you move the folder and so the shortcut doesn't work, just run "install.bat" again.
The generated shortcut can be put anywhere

## Everyone

Setup:

`poetry install`

Run:

`poetry run python studdybudy` (substituting python with pythonw lets you close the cmd window)

# SoundRandomiser functionality
randomly decides to play a random sound effect
place sfx to loop over in the folder `./media/randomiser` (subdirectories are ok!)
these must be formatted as ".wav"

Pressing load will add all .wav files from the subfolders in the `sfx directory` to the current list of loaded sfx. Sfx are grouped via their sub-directory and can be enabled/disabled based on this separation by selecting it in the `sub-directory` drop down. If a subfolder has already been loaded, pressing load will reload that folders entry (sfx shouldn't just doubled up anymore).

* probablity is the chance that a sound will be played, then it is an equal choice between all sfx loaded from the sfx dir
* frequency is how much time will pass between each roll (just ignore that it actually describes the period)

# SoundLooper functionality
load in a song and endlessly loop it!
over here, we use the `./media/looper` folder for songs (then you can choose the song by typing just the filename into the program's textbox)
implements https://github.com/arkrow/PyMusicLooper to automagically select ideal points of the song to loop between,,,
format is not as strict here

* type filename
* press load, wait for a sliver of time
* press autoset loop, wait many slivers of time
* now you can use play/pause/stop

# To do:
SR
* make the directory boxes scroll to the right as this is the more informative part of the string...

SL
* browse/list files in the directory
* find closest file matching filename
* allow manual loop point selection
* cache previous loop points for faster song loading

idks
* can I volume controls?? apparently not for sounddevice specifically, so you need to use volume mixer, but maybe I can at some point set the volume mixer from within python
* memory of previous directories and filename restored when opening the program
