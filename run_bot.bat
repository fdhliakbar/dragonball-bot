@echo off
echo ========================================
echo Dragon Ball Discord Bot
echo ========================================

REM Check if .env file exists
if not exist .env (
    echo Error: File .env tidak ditemukan!
    echo Silakan buat file .env dan masukkan DISCORD_TOKEN Anda.
    echo.
    echo Contoh isi .env:
    echo DISCORD_TOKEN=your_bot_token_here
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo Error: Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu.
    pause
    exit /b 1
)

echo Starting Dragon Ball Bot...
echo.
.venv\Scripts\python.exe main.py

pause
