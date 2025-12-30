@echo off
REM Build DOCX document(s) from markdown
REM For multilanguage projects: builds all languages by default
REM Use: build_docx.bat [--lang en|it|all]

setlocal
cd /d "%~dp0"

set "LOG=%~dp0build_docx.log"

rem Capture all output to a log so it can be viewed even after the window closes.
python tools\build_docx.py %* >"%LOG%" 2>&1
set "RC=%errorlevel%"

echo ===== build_docx log (%LOG%) =====
type "%LOG%"
echo ===== end log =====
echo.
if %RC% neq 0 (
  echo Build failed (exit %RC%). Log saved to:
  echo   %LOG%
  echo Opening log in Notepad for easier copying...
  start "" "%LOG%"
) else (
  echo Build finished (exit %RC%). Log saved to:
  echo   %LOG%
)

echo.

