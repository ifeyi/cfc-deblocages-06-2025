#!/bin/bash
# Debug script to check container status

echo "=== CFC Container Debug ==="
echo ""

echo "1. Docker Compose PS:"
docker-compose ps
echo ""

echo "2. Docker PS (all CFC containers):"
docker ps -a --filter "name=cfc_"
echo ""

echo "3. Checking specific backend container:"
BACKEND_RUNNING=$(docker-compose ps -q cfc_backend)
echo "Backend container ID: '$BACKEND_RUNNING'"

if [ -z "$BACKEND_RUNNING" ]; then
    echo "❌ Backend container ID is empty"
else
    echo "✅ Backend container ID found"
    
    # Check if it's actually running
    CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' cfc_backend 2>/dev/null)
    echo "Container status: $CONTAINER_STATUS"
fi

echo ""
echo "4. Alternative check using docker ps:"
BACKEND_RUNNING_ALT=$(docker ps -q --filter "name=cfc_backend")
echo "Backend running (docker ps): '$BACKEND_RUNNING_ALT'"

echo ""
echo "5. Check if services are defined in docker-compose:"
docker-compose config --services | grep -E "(backend|cfc_backend)"

echo ""
echo "6. Current working directory:"
pwd
echo ""
echo "7. Docker-compose file exists:"
ls -la docker-compose.yml

echo ""
echo "=== Recommendations ==="
if [ -z "$BACKEND_RUNNING" ]; then
    echo "❌ Backend not running. Try:"
    echo "   docker-compose up -d"
    echo "   or"
    echo "   make up"
else
    echo "✅ Backend appears to be running"
    echo "Try running migration directly:"
    echo "   docker-compose exec cfc_backend alembic upgrade head"
fi