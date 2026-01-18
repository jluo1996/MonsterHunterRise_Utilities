@echo off

cd /d "%~dp0..\.."

set "appName=%~1" 
set "versionMajor=%~2"
set "versionMinor=%~3"
set "versionBuild=%~4"
set "versionRevision=%~5"
set "versionFile=%~dp0..\version_info.txt"

echo Writing version info ...
python314\python.exe "build\scripts\prebuild.py" "%appName%" "%versionMajor%" "%versionMinor%" "%versionBuild%" "%versionRevision%" %versionFile%

echo Generating "%appName%.exe" in "%~f0" ...
 
python314\python.exe -m PyInstaller --onefile --noconsole --version-file "build\version_info.txt" --add-data "Utilities\Resources;\Resources" --name="%appName%" "Utilities\MainPy.py"