@echo off
SET PROJECT_ROOT=release_sentinel

echo [*] Creating project structure for %PROJECT_ROOT%...

:: Create Directories
mkdir %PROJECT_ROOT%\src\release_sentinel\checks
mkdir %PROJECT_ROOT%\tests

:: Create Root Files
type nul > %PROJECT_ROOT%\pyproject.toml
type nul > %PROJECT_ROOT%\README.md
type nul > %PROJECT_ROOT%\.gitignore

:: Create Source Files
type nul > %PROJECT_ROOT%\src\release_sentinel\__init__.py
type nul > %PROJECT_ROOT%\src\release_sentinel\cli.py
type nul > %PROJECT_ROOT%\src\release_sentinel\logging.py
type nul > %PROJECT_ROOT%\src\release_sentinel\config.py
type nul > %PROJECT_ROOT%\src\release_sentinel\core.py

:: Create Check Module Files
type nul > %PROJECT_ROOT%\src\release_sentinel\checks\git.py
type nul > %PROJECT_ROOT%\src\release_sentinel\checks\env.py
type nul > %PROJECT_ROOT%\src\release_sentinel\checks\system.py
type nul > %PROJECT_ROOT%\src\release_sentinel\checks\api.py
type nul > %PROJECT_ROOT%\src\release_sentinel\checks\result.py

:: Create Test Files
type nul > %PROJECT_ROOT%\tests\test_git.py
type nul > %PROJECT_ROOT%\tests\test_env.py
type nul > %PROJECT_ROOT%\tests\test_system.py
type nul > %PROJECT_ROOT%\tests\test_core.py

echo [!] Structure created successfully.
pause