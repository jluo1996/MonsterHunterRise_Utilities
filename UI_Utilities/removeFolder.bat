@echo off
REM Hard-coded folder name
set foldername=reframework

REM Destination folder passed as parameter
REM %1 = destination path
set "destFolder=%~1"

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Validate destination parameter
if "%destFolder%"=="" (
    echo ERROR: Destination path not provided.
    echo Usage: %scriptDir%removeFolder.bat 
    exit /b
)

REM Build full path to the folder in the parent directory
set targetFolder=%destFolder%%foldername%

REM Delete the folder and all its contents
if exist "%targetFolder%" (
    rmdir /S /Q "%targetFolder%"
    echo %targetFolder% deleted successfully.
) else (
    echo %targetFolder% does not exist.
)
