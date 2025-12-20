@echo off
REM Hard-coded file name
set filename=dinput8.dll

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Build full path to source file
set sourceFile=%scriptDir%%filename%

REM Build full path to destination (parent folder of the script folder)
set parentFolder=%scriptDir%..\

REM Copy the file to the parent directory
copy "%sourceFile%" "%parentFolder%" /Y

echo File "%filename%" copied to parent folder successfully.
