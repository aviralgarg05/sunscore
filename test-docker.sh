#!/bin/bash

echo "🐳 Testing SunScore Docker deployment..."

# Check available disk space
available_space=$(df -h . | awk 'NR==2 {print $4}')
echo "💾 Available disk space: $available_space"

# Clean up Docker to free space
echo "🧹 Cleaning up Docker to free space..."
docker system prune -f
docker image prune -f

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env with your actual API credentials"
        exit 1
    else
        echo "❌ No .env.example found. Please create .env manually"
        exit 1
    fi
fi

# Validate environment variables
if grep -q "your_api_key_here" .env || grep -q "your_email@example.com" .env; then
    echo "❌ Please update .env with real values (not placeholder values)"
    exit 1
else
    echo "✅ Environment variables appear to be configured"
fi

# Create sample data file if needed
if [ ! -f "sample_zips.csv" ]; then
    echo "📝 Creating sample ZIP data..."
    cat > sample_zips.csv << 'EOF'
zip,lat,lng,state_id,city
90210,34.0901,-118.4065,CA,Beverly Hills
10001,40.7505,-73.9934,NY,New York
60601,41.8827,-87.6233,IL,Chicago
EOF
fi

# Build Docker image with minimal context
echo "🔨 Building Docker image..."
docker build -t sunscore:latest . --no-cache

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
    
    # Test run (dry run mode) - fixed the command format
    echo "🧪 Testing Docker container..."
    docker run --rm \
        -e NSRDB_API_KEY="${NSRDB_API_KEY:-test}" \
        -e NSRDB_EMAIL="${NSRDB_EMAIL:-test@example.com}" \
        -v "$(pwd)/sample_zips.csv:/app/sample_zips.csv" \
        sunscore:latest python -c "
import os
print('🔧 Running container validation...')
print(f'API Key set: {bool(os.getenv(\"NSRDB_API_KEY\"))}')
print(f'Email set: {bool(os.getenv(\"NSRDB_EMAIL\"))}')
print('✅ Container test completed')
"
    
    if [ $? -eq 0 ]; then
        echo "✅ Docker test successful!"
        echo "🚀 To run the full application:"
        echo "   docker run --env-file .env -v \$(pwd)/uszips.csv:/app/uszips.csv sunscore:latest"
    else
        echo "❌ Docker test failed"
        exit 1
    fi
else
    echo "❌ Docker build failed"
    echo "💡 Try freeing up disk space and run: docker system prune -a"
    exit 1
fi

echo "✅ Test completed!"
            sleep 5
            timeout=$((timeout - 5))
        done

        if [ $timeout -le 0 ]; then
            echo "❌ MongoDB failed to start within 60 seconds"
            docker-compose logs mongo
            exit 1
        fi

        echo "🌞 Running SunScore application..."
        docker-compose up sunscore

        echo "🧹 Cleaning up..."
        docker-compose down
        echo "✅ Test completed!"
    else
        echo "❌ Docker test failed"
        exit 1
    fi
else
    echo "❌ Docker build failed"
    exit 1
fi
echo "✅ Test completed!"
