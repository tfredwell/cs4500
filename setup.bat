REM inspired by https://gist.githubusercontent.com/jsyeo/6276896/raw/cef60b4871ffb365184da11601c0ba00adf7690b/install_dist_pip.bat

set PACKAGE_PATH=%cd%

cd %USERPROFILE%
 
REM create the venv
 
C:\Python37\Scripts\virtualenv %USERPROFILE%\venv
 
REM activate the venv, install distribute, install pip, create IDLE shortcut in desktop, install PILLOW

powershell.exe -Command $shortcut = (New-Object -comObject WScript.Shell).CreateShortcut('%USERPROFILE%\Desktop\CozmoTasteGame.lnk'); $shortcut.TargetPath = '%PACKAGE_PATH%\run_game.bat'; $shortcut.WorkingDirectory = '%PACKAGE_PATH%'; $shortcut.Save() 
%USERPROFILE%\venv\Scripts\activate.bat & pip install -r %PACKAGE_PATH%\requirements.txt