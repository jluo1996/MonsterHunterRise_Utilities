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
set "targetFile=%destFolder%\%filename%"

@REM if not exist "%targetFile%" (
@REM     echo ERROR: File %targetFile% does not exist.
@REM     exit
@REM )

REM Delete the file
echo Deleting %targetFile%...
del "%targetFile%"
echo %targetFile% deleted successfully.