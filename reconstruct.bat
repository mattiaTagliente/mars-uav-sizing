@echo off
setlocal enabledelayedexpansion

REM Reconstruct markdown document(s) from split sections
REM For multilanguage projects: processes all languages by default
REM Use: reconstruct.bat [en|it|all] or reconstruct.bat [--lang en|it|all]

cd /d "%~dp0"

REM Create backups directory if it doesn't exist
if not exist "backups" mkdir "backups"

REM Generate timestamp for backups
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set datestr=%%c%%b%%a
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set timestr=%%a%%b
)
set timestamp=!datestr!_!timestr!

REM Backup existing markdown files (common document names)
for %%f in (drone.md drone_it.md) do (
    if exist "%%f" (
        copy "%%f" "backups\%%~nf_!timestamp!.md" >nul 2>&1
        if not errorlevel 1 (
            echo Backup created: backups\%%~nf_!timestamp!.md
        )
    )
)

REM Handle language argument - support both simple (en) and full (--lang en) formats
set ARGS=%*
if "%~1"=="" goto :run_python
if "%~1"=="en" set ARGS=--lang en
if "%~1"=="it" set ARGS=--lang it
if "%~1"=="all" set ARGS=--lang all

:run_python
REM Run the reconstruction script with processed arguments
python .\tools\join_sections.py %ARGS%

