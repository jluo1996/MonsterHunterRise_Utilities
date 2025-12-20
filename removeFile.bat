@echo off
REM Hard-coded file name
set filename=dinput8.dll

REM Get the directory where the script is located
set scriptDir=%~dp0

REM Build full path to the file in the parent folder
set targetFile=%scriptDir%..\%filename%

REM Delete the file
if exist "%targetFile%" (
    del "%targetFile%"
    echo File "%filename%" deleted from parent folder successfully.
) else (
    echo File "%filename%" does not exist in the parent folder.
)