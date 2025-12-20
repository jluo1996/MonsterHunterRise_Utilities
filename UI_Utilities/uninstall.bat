@echo off
REM Hard-coded expected parent folder name
set expectedParent=MonsterHunterRise

REM Get the full path of the parent folder
for %%F in ("%~dp0..") do set parentFolderName=%%~nF

REM Check if parent folder name matches
if /I "%parentFolderName%"=="%expectedParent%" (
    echo Running scripts...

    REM Hard-coded batch file names
    set firstFile=removeFile.bat
    set secondFile=removeFolder.bat

    REM Call the first batch file
    call "%firstFile%"

    REM Call the second batch file
    call "%secondFile%"

    echo Mod has been uninstalled.
) else (
    echo Please run this under the game install directory. It should be a folder named "%expectedParent%".
    echo Uninstallation failed.
    pause
)


