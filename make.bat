@echo off
REM Make.bat for Mikufetch 🐱‍💻
REM Usage: make.bat [command]
REM Commands: install, test, docs, clean, run, help

SET PYTHON=python
SET PACKAGE=mikufetch
SET DOCS_SRC=docs
SET DOCS_BUILD=docs\_build

IF "%1"=="" GOTO help

IF /I "%1"=="help" (
    GOTO help
) ELSE IF /I "%1"=="install" (
    GOTO install
) ELSE IF /I "%1"=="test" (
    GOTO test
) ELSE IF /I "%1"=="docs" (
    GOTO docs
) ELSE IF /I "%1"=="clean" (
    GOTO clean
) ELSE IF /I "%1"=="run" (
    GOTO run
) ELSE (
    ECHO Unknown command: %1
    GOTO end
)

:help
ECHO Available commands:
ECHO   make.bat install    - Install Mikufetch locally
ECHO   make.bat test       - Run tests with pytest
ECHO   make.bat docs       - Build HTML docs with Sphinx
ECHO   make.bat clean      - Clean build artifacts and cache
ECHO   make.bat run        - Run Mikufetch locally
GOTO end

:install
%PYTHON% -m pip install --upgrade pip
%PYTHON% -m pip install -e .
GOTO end

:test
REM Install pytest if missing
%PYTHON% -m pip install --user pytest
%PYTHON% -m pytest tests
GOTO end

:docs
%PYTHON% -m pip install sphinx
%PYTHON% -m pip install sphinx_rtd_theme
%PYTHON% -m sphinx -b html %DOCS_SRC% %DOCS_BUILD%
GOTO end

:clean
rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q *.egg-info
rmdir /S /Q %DOCS_BUILD%
for /D %%d in (__pycache__) do rmdir /S /Q "%%d"
for /D %%d in (.pytest_cache) do rmdir /S /Q "%%d"
GOTO end

:run
%PYTHON% -m %PACKAGE%
GOTO end

:end
