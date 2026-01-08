@echo off
SETLOCAL EnableDelayedExpansion

:: --- Configuration ---
SET VENV_DIR=.venv
SET PYTHON_EXE=python
SET PROJECT_NAME=release_sentinel

:menu
cls
echo ====================================================
echo          RELEASE SENTINEL DEVELOPMENT MENU
echo ====================================================
echo 1. Setup Environment (venv + install)
echo 2. Run Tests (pytest)
echo 3. Run Release Sentinel (CLI)
echo 4. Lint Code (ruff/flake8)
echo 5. Clean Build Artifacts
echo 6. Exit
echo ====================================================
set /p opt="Select an option (1-6): "

if "%opt%"=="1" goto setup
if "%opt%"=="2" goto test
if "%opt%"=="3" goto run
if "%opt%"=="4" goto lint
if "%opt%"=="5" goto clean
if "%opt%"=="6" goto end

:setup
echo [*] Creating virtual environment...
%PYTHON_EXE% -m venv %VENV_DIR%
echo [*] Installing project in editable mode with dev dependencies...
%VENV_DIR%\Scripts\pip install -e .[dev]
echo [!] Setup complete.
pause
goto menu

:test
echo [*] Running tests via pytest...
%VENV_DIR%\Scripts\pytest tests/
pause
goto menu

:run
echo [*] Launching Release Sentinel CLI...
%VENV_DIR%\Scripts\python -m %PROJECT_NAME%.cli
pause
goto menu

:lint
echo [*] Checking code style...
%VENV_DIR%\Scripts\python -m ruff check .
pause
goto menu

:clean
echo [*] Cleaning up __pycache__ and build files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
if exist .pytest_cache rd /s /q .pytest_cache
if exist dist rd /s /q dist
if exist *.egg-info rd /s /q *.egg-info
echo [!] Cleanup finished.
pause
goto menu

:end
exit