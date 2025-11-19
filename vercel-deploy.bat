@echo off
REM Vercel deployment optimization script for Windows

echo Starting Vercel deployment optimization...

REM Set environment variables for Vercel
set VERCEL_ENV=production

REM Use the reduced requirements file for Vercel deployment
if exist "requirements-vercel.txt" (
    echo Using reduced requirements for Vercel deployment
    ren requirements.txt requirements-full.txt
    copy requirements-vercel.txt requirements.txt
)

echo Vercel deployment optimization completed