@echo off

set "appName=%~1"

echo Generating "%appName%.exe" in "%~f0" ...

python314\python.exe -m PyInstaller --onefile --add-data "Utilities\Resources;\Resources" --name="%appName%" "Utilities\Main\MainGUI.py"