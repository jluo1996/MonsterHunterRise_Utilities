@echo off

cd /d "%~dp0..\.."

set "appName=%~1" 
set "pythonPath=%~2"

echo Generating "%appName%.exe" in "%~f0" ...

%pythonPath% -m PyInstaller --onefile --noconsole --version-file "build\version_info.txt" --add-data "Utilities\Resources;\Resources" --name="%appName%" "Utilities\MainPy.py"

REM ---- Stop if PyInstaller failed ----
if errorlevel 1 (
    echo ERROR: PyInstaller failed.
    exit /b 1
)

echo Build completed successfully.
exit /b 0