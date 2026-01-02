@echo off
setlocal EnableExtensions

rem Script portabile per eseguire l'analisi MATLAB da qualsiasi percorso.
rem Uso: run_matlab_analysis.bat [it|en]

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "ROOT_DIR=%SCRIPT_DIR%"

set "LANG=it"
if /i "%~1"=="en" set "LANG=en"
if /i "%~1"=="it" set "LANG=it"

set "MATLAB_DIR=%ROOT_DIR%\src\matlab_scripts"
set "FIG_DIR=%MATLAB_DIR%\figures"

set "MARS_UAV_ROOT=%ROOT_DIR%"
if exist "%ROOT_DIR%\src\mars_uav_sizing\config" (
    set "MARS_UAV_CONFIG_DIR=%ROOT_DIR%\src\mars_uav_sizing\config"
) else if exist "%MATLAB_DIR%\config" (
    set "MARS_UAV_CONFIG_DIR=%MATLAB_DIR%\config"
)

if defined MATLAB_EXE (
    set "MATLAB_CMD=%MATLAB_EXE%"
) else (
    where matlab >nul 2>nul
    if not errorlevel 1 (
        set "MATLAB_CMD=matlab"
    ) else (
        for %%V in (R2025b R2025a R2024b R2024a R2023b R2023a) do (
            if not defined MATLAB_CMD if exist "C:\Program Files\MATLAB\%%V\bin\matlab.exe" (
                set "MATLAB_CMD=C:\Program Files\MATLAB\%%V\bin\matlab.exe"
            )
        )
    )
)

if not defined MATLAB_CMD (
    echo MATLAB non trovato. Installare MATLAB o impostare la variabile MATLAB_EXE.
    echo Esempio: setx MATLAB_EXE "C:\Program Files\MATLAB\R2025a\bin\matlab.exe"
    exit /b 1
)

set "MATLAB_CMD_LINE=restoredefaultpath; addpath(genpath('%MATLAB_DIR%')); cd('%MATLAB_DIR%'); run_analysis('figures_lang','%LANG%','figures_output_dir','%FIG_DIR%');"
"%MATLAB_CMD%" -batch "%MATLAB_CMD_LINE%"

exit /b %ERRORLEVEL%
