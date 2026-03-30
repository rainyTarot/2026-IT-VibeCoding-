@echo off
setlocal

set "GAME_DIR=%~dp0SpaceFarmMolePatrol"
set "GAME_EXE=%GAME_DIR%\SpaceFarmMolePatrol.exe"

if exist "%GAME_EXE%" (
    start "" "%GAME_EXE%"
    goto :end
)

echo Executable not found:
echo %GAME_EXE%
pause

:end
endlocal
