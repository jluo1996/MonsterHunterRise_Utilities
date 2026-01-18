@echo off

cd /d "%~dp0..\.."

set "appName=%~1" 
set "versionMajor=%~2"
set "versionMinor=%~3"
set "versionBuild=%~4"
set "versionRevision=%~5"
set "versionFile=%~dp0..\version_info.txt"

@REM echo Writing version info ...
@REM python314\python.exe "build\scripts\prebuild.py" "%appName%" "%versionMajor%" "%versionMinor%" "%versionBuild%" "%versionRevision%" %versionFile%

@REM REM ---- Stop if prebuild failed ----
@REM if errorlevel 1 (
@REM     echo ERROR: prebuild.py failed. Aborting build.
@REM     exit /b 1
@REM )

echo Generating "%appName%.exe" in "%~f0" ...
 
python314\python.exe -m PyInstaller --onefile --noconsole --version-file "build\version_info.txt" --add-data "Utilities\Resources;\Resources" --name="%appName%" "Utilities\MainPy.py"

REM ---- Stop if PyInstaller failed ----
if errorlevel 1 (
    echo ERROR: PyInstaller failed.
    exit /b 1
)

echo Build completed successfully.
exit /b 0