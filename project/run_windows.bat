@echo off
echo Setting up Python virtual environment...

REM Check if venv exists
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run the game
echo Starting the game...
python arcade_games.py

REM Deactivate virtual environment
deactivate

REM Keep window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo An error occurred. Press any key to exit.
    pause > nul
)
