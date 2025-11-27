@echo off
:: make the folder that contains this bat the current directory
pushd "%~dp0"

:: ---- environment variables ----
set "OPENAI_BASE_URL=http://localhost:13141/v1"
set "OPENAI_MODEL=model"
:: absolute path to the PDF directory
set "EXAMPLE_DOCS_FILE_DIR=%~dp0docs\"

:: ---- paths to the shipped interpreter and script ----
set "PY_EMBED=%~dp0python-3.10\python.exe"
set "MAIN_PY=%~dp0main.py"

:: ---- launch ----
"%PY_EMBED%" "%MAIN_PY%"
popd
