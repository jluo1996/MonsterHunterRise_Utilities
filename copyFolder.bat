@echo off
REM Hard-coded folder name
set foldername=reframework

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Build full path to source folder
set sourceFolder=%scriptDir%%foldername%

REM Build full path to destination (parent folder of the script folder)
set parentFolder=%scriptDir%..\

REM Copy the folder to the parent directory
xcopy "%sourceFolder%" "%parentFolder%%foldername%" /E /I /H /Y

echo Folder "%foldername%" copied to parent folder successfully.
