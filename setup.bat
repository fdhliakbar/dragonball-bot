@echo off
echo ========================================
echo Dragon Ball Bot Setup
echo ========================================

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install packages
echo Installing dependencies...
.venv\Scripts\pip.exe install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE > .env
    echo.
    echo File .env telah dibuat!
    echo Silakan edit file .env dan masukkan Discord Bot Token Anda.
)

echo.
echo ========================================
echo Setup completed!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file dan masukkan Discord Bot Token
echo 2. Run bot dengan: run_bot.bat
echo.
pause
