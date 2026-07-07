@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ==========================================
echo   AirportGame - Installation & Start
echo ==========================================

set "PYTHON_CMD="

REM --- Python pruefen (zuerst direktes Python, dann Python-Launcher) ---
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=python"
    goto :found_python
)

py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=py"
    goto :found_python
)

echo Python wurde nicht gefunden. Installiere Python 3.11 ueber winget...
winget install --id Python.Python.3.11 -e --accept-package-agreements --accept-source-agreements --silent >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python wurde installiert.
    start "" cmd /c "echo Starte das Skript erneut... && call \"%~f0\""
    exit /b
)

echo.
echo Fehler: Python konnte nicht automatisch installiert werden.
echo Bitte Python 3.9+ manuell installieren: https://www.python.org/downloads/
echo.
pause
exit /b 1

:found_python
echo Python gefunden:
%PYTHON_CMD% --version
echo.

REM --- Setup ausfuehren ---
echo Fuehre Setup aus...
%PYTHON_CMD% setup.py
if %ERRORLEVEL% NEQ 0 (
    echo Setup fehlgeschlagen.
    pause
    exit /b 1
)

echo Setup abgeschlossen.
echo.

REM --- Spiel starten ---
echo Starte AirportGame...
%PYTHON_CMD% run.py

endlocal
pause
