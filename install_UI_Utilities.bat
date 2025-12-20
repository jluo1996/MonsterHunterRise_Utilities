@echo off

set "scriptDir=%~dp0"
set "scriptName=%~nx0"

set "uiUtilitiesDir=%scriptDir%UI_Utilities\"
set "uiUtilitiesScript=%uiUtilitiesDir%install.bat"

echo Running from directory: "%scriptDir%%scriptName%"

REM Ask user to enter or paste a full path
set /p gameInstallPath=Please enter or paste the full path of the game install directory: 

REM Check if user entered something
if "%gameInstallPath%"=="" (
    echo No path entered. Exiting...
    exit /b
)

REM Display the entered path
echo You entered: "%gameInstallPath%"

REM Example: check if the path exists
if exist "%gameInstallPath%" (
    call "%uiUtilitiesScript%" "%gameInstallPath%\"
) else (
    echo The path does NOT exist.
)

pause
