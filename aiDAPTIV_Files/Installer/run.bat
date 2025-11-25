@echo off
REM Change current directory to where the batch file is located
pushd "%~dp0"

REM Set environment variables
set "OPENAI_BASE_URL=http://localhost:8080/v1"
set "OPENAI_MODEL=model"
set "EXAMPLE_DOCS_FILE_DIR=%~dp0..\Example\Files\"

REM Define path to your embeddable python.exe (relative to the batch file)
set "PY_EMBED=%~dp0..\python-3.10\python.exe"

REM Run your Python script (also relative to the batch file)
"%PY_EMBED%" "%~dp0..\main.py"

REM Return to the original directory
popd
