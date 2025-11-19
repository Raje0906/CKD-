#!/bin/bash
# Vercel deployment optimization script

echo "Starting Vercel deployment optimization..."

# Set environment variables for Vercel
export VERCEL_ENV="production"

# Use the reduced requirements file for Vercel deployment
if [ -f "requirements-vercel.txt" ]; then
    echo "Using reduced requirements for Vercel deployment"
    mv requirements.txt requirements-full.txt
    cp requirements-vercel.txt requirements.txt
fi

echo "Vercel deployment optimization completed"