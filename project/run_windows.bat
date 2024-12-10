@echo off
echo Setting up arcade games...

REM Download requirements.txt and arcade_games.py
echo Downloading files...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Coolbossco/Coolbossco/main/project/requirements.txt' -OutFile 'requirements.txt'"
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Coolbossco/Coolbossco/main/project/arcade_games.py' -OutFile 'arcade_games.py'"

REM Check if downloads were successful
if not exist requirements.txt (
    echo Failed to download requirements.txt
    pause
    exit /b 1
)
if not exist arcade_games.py (
    echo Failed to download arcade_games.py
    pause
    exit /b 1
)

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
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

REM Clean up downloaded files
del requirements.txt
del arcade_games.py

REM Keep window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo An error occurred. Press any key to exit.
    pause > nul
)
