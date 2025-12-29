@echo off

REM Hard-coded folder name
set foldername=reframework

REM Destination folder passed as parameter
REM %1 = destination path
set "destFolder=%~1"

REM Get the directory where the script is located
set "scriptDir=%~dp0"

REM Validate destination parameter
if "%destFolder%"=="" (
    echo ERROR: Destination path not provided.
    echo Usage: %scriptDir%copyFolder.bat 
    exit /b
)

REM Build full path to source folder
set sourceFolder=%scriptDir%%foldername%

echo Copying folder "%foldername%" to "%destFolder%%foldername%"...

REM Copy the folder to the parent directory
xcopy "%sourceFolder%" "%destFolder%%foldername%" /E /I /H /Y

echo Folder "%foldername%" copied to "%destFolder%%foldername%" successfully.
