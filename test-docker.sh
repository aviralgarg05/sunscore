#!/bin/bash

echo "🐳 Testing SunScore Docker deployment..."

# Validate disk space
available_space=$(df -h . | awk 'NR==2 {print $4}')
echo "💾 Available disk space: $available_space"

# Cleanup
echo "🧹 Cleaning up Docker environment..."
docker system prune -f
docker image prune -f

# Check for required files
if [ ! -f ".env" ]; then
    echo "❌ Missing .env file"
    exit 1
fi

if [ ! -f "uszips.csv" ]; then
    echo "❌ uszips.csv not found"
    exit 1
fi

if [ ! -d "shapefiles" ] || [ $(find shapefiles -name "*.shp" | wc -l) -eq 0 ]; then
    echo "❌ Shapefiles directory or .shp file missing"
    exit 1
fi

echo "✅ All required files are present"

# Build image
echo "🔨 Building Docker image..."
docker build -t sunscore:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

# Run validation container
echo "🧪 Validating container environment..."
docker run --rm --env-file .env sunscore:latest