@echo off

set "scriptDir=%~dp0"
set "scriptName=%~nx0"

set "scriptLogName=install_UI_Utilities_log.txt"

REM Get date in YYYY-MM-DD format (ignore day name)
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set "logDate=%%c-%%a-%%b"
)

REM Get time in HH-MM-SS format (ignore milliseconds)
for /f "tokens=1-3 delims=:." %%a in ("%time%") do (
    set "logTime=%%a-%%b-%%c"
)

REM Build timestamped log file name
set "scriptLogPath=%scriptDir%\LogFiles\install_UI_Utilities_%logDate%_%logTime%.txt"

set "uiUtilitiesDir=%scriptDir%\UI_Utilities\"
set "uiUtilitiesScript=%uiUtilitiesDir%\install.bat"

echo Running from directory: "%scriptDir%%scriptName%"

REM Ensure the LogFiles folder exists
if not exist "%scriptDir%\LogFiles" (
    mkdir "%scriptDir%\LogFiles"
)

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
    for /f "delims=" %%A in ('call "%uiUtilitiesScript%" "%gameInstallPath%\" 2^>^&1') do (
    echo [%date% %time%] %%A >> "%scriptLogPath%"
    )
    echo UI Utilities has been installed.
) else (
    echo The path does NOT exist.
)

pause
