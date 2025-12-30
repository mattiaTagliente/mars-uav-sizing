@echo off
REM Split markdown document(s) into sections
REM For multilanguage projects: processes all languages by default
REM Use: split.bat [--lang en|it|all]

cd /d "%~dp0"
python .\tools\split_sections.py %*

