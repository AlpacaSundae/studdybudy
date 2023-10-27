git pull
poetry config --local virtualenvs.in-project true
poetry install

:: this creates a shortcut to run the program
:: nice and shrimple, also hides the cmd window
set TARGET='%cd%\.venv\Scripts\pythonw.exe'
set ARGS='studdybudy'
set WPATH='%cd%'
set SHORTCUT='studdybudy.lnk'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.Arguments = %ARGS%; $S.WorkingDirectory = %WPATH%; $S.Save()"