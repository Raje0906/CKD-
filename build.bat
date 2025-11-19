@echo off
REM Build script for optimizing Vercel deployment on Windows

echo Starting build optimization...

REM Clean up any existing build artifacts
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Create necessary directories
mkdir build

REM Copy only essential files for deployment
xcopy templates build\templates\ /E /I /H
xcopy static build\static\ /E /I /H
xcopy models build\models\ /E /I /H
copy app.py build\
copy index.py build\
copy requirements.txt build\
copy vercel.json build\
if exist runtime.txt copy runtime.txt build\

REM Remove unnecessary files from models directory in build
del /q build\models\*.pyc 2>nul
for /d %%i in (build\models\__pycache__) do rmdir /s /q "%%i" 2>nul

echo Build optimization completed.