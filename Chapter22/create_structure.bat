@echo off
echo Creating Deploy Guard folder structure...

:: Root Files
mkdir deploy_guard
cd deploy_guard
type nul > pyproject.toml
type nul > README.md
type nul > .gitignore

:: Source Directory and Subpackages
mkdir src\deploy_guard\core
mkdir src\deploy_guard\notes

type nul > src\deploy_guard\__init__.py
type nul > src\deploy_guard\cli.py
type nul > src\deploy_guard\logging.py
type nul > src\deploy_guard\config.py

:: Core Logic Files
type nul > src\deploy_guard\core\env_gate.py
type nul > src\deploy_guard\core\release_guard.py
type nul > src\deploy_guard\core\health_checks.py
type nul > src\deploy_guard\core\api_checks.py
type nul > src\deploy_guard\core\deploy.py

:: Notes
type nul > src\deploy_guard\notes\release_notes.py

:: Tests
mkdir tests
type nul > tests\test_env_gate.py
type nul > tests\test_release_guard.py
type nul > tests\test_health_checks.py
type nul > tests\test_api_checks.py
type nul > tests\test_deploy.py

echo Structure created successfully!
pause