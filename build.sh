#!/bin/bash
# Build script for optimizing Vercel deployment

echo "Starting build optimization..."

# Clean up any existing build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Create necessary directories
mkdir -p build/

# Copy only essential files for deployment
cp -r templates/ build/
cp -r static/ build/
cp -r models/ build/
cp app.py build/
cp index.py build/
cp requirements.txt build/
cp vercel.json build/
cp runtime.txt build/ 2>/dev/null || echo "No runtime.txt file"

# Remove unnecessary files from models directory in build
rm -f build/models/ckd_model.pyc
rm -rf build/models/__pycache__/

echo "Build optimization completed."