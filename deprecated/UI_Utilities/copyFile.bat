@echo off

REM Hard-coded file name
set filename=dinput8.dll

REM Destination folder passed as parameter
REM %1 = destination path
set "destFolder=%~1"

REM Get the directory where the script is located
set "scriptDir=%~dp0"

REM Validate destination parameter
if "%destFolder%"=="" (
    echo ERROR: Destination path not provided.
    echo Usage: %scriptDir%copyFile.bat 
    exit /b
)

REM Build full path to source file
set "sourceFile=%scriptDir%%filename%"

echo Copying "%filename%" to "%destFolder%"...

REM Copy the file to the destination folder
copy /Y "%sourceFile%" "%destFolder%"

echo File "%filename%" has been copied to "%destFolder%".
