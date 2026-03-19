@echo off
echo Starting Video Re-creation Agent...

if not exist .env (
    echo .env not found. Copy .env.example to .env first.
    exit /b 1
)

mkdir data\videos 2>nul
mkdir data\audio 2>nul
mkdir data\outputs 2>nul

echo Server starting at http://127.0.0.1:8000/
python backend\main.py
