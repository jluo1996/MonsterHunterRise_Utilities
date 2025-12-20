@echo off

REM Destination folder passed as parameter
REM %1 = destination path
set "destFolder=%~1"

REM Get the directory where the script is located
set "scriptDir=%~dp0"

REM Validate destination parameter
if "%destFolder%"=="" (
    echo ERROR: Destination path not provided.
    echo Usage: %scriptDir%install.bat 
    exit /b
)

REM Hard-coded batch file names
set firstFile=copyFile.bat
set secondFile=copyFolder.bat

REM Call the first batch file
call "%scriptDir%%firstFile%" "%destFolder%"

REM Call the second batch file
call "%scriptDir%%secondFile%" "%destFolder%"

echo UI Utilities has been installed.