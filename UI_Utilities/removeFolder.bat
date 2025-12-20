@echo off
REM Hard-coded folder name
set foldername=reframework

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Build full path to the folder in the parent directory
set targetFolder=%scriptDir%..\%foldername%

REM Delete the folder and all its contents
if exist "%targetFolder%" (
    rmdir /S /Q "%targetFolder%"
    echo Folder "%foldername%" deleted from parent folder successfully.
) else (
    echo Folder "%foldername%" does not exist in the parent folder.
)
