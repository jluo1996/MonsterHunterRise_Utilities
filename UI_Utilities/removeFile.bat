@echo off
REM Hard-coded file name
set filename=dinput8.dll

REM Destination folder passed as parameter
REM %1 = destination path
set "destFolder=%~1"

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Validate destination parameter
if "%destFolder%"=="" (
    echo ERROR: Destination path not provided.
    echo Usage: %scriptDir%removeFile.bat 
    exit /b
)

REM Build full path to the file in the parent folder
set targetFile=%destFolder%%filename%

REM Delete the file
if exist "%targetFile%" (
    del "%targetFile%"
    echo %targetFile% deleted successfully.
) else (
    echo %targetFile% does not exist.
)