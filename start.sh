#!/bin/bash

# AI Debug Assistant - Startup Script
# This script provides easy commands to run the application in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_warning "Please edit .env file and add your OPENAI_API_KEY"
        else
            print_error ".env.example not found. Please create .env file manually."
            exit 1
        fi
    fi
    
    if ! grep -q "OPENAI_API_KEY=" .env || grep -q "OPENAI_API_KEY=$" .env; then
        print_warning "OPENAI_API_KEY not set in .env file. AI features will not work."
    fi
}

# Function to show usage
show_usage() {
    echo "AI Debug Assistant - Startup Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  dev         Start development environment (with hot reload)"
    echo "  prod        Start production environment"
    echo "  build       Build Docker images"
    echo "  stop        Stop all services"
    echo "  clean       Clean up Docker containers and images"
    echo "  logs        Show logs from all services"
    echo "  test        Run tests for all modules"
    echo "  backend     Start only backend service"
    echo "  frontend    Start only frontend service"
    echo "  health      Check service health"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev      # Start development environment"
    echo "  $0 prod     # Start production environment"
    echo "  $0 logs     # View logs"
    echo "  $0 clean    # Clean up everything"
}

# Function to start development environment
start_dev() {
    print_status "Starting development environment..."
    check_docker
    check_env
    
    print_status "Building and starting services..."
    docker-compose -f docker-compose.dev.yml up --build
}

# Function to start production environment
start_prod() {
    print_status "Starting production environment..."
    check_docker
    check_env
    
    print_status "Building and starting services..."
    docker-compose --profile production up --build -d
    
    print_success "Production environment started!"
    print_status "Frontend: http://localhost"
    print_status "Backend API: http://localhost:8000"
    print_status "Use '$0 logs' to view logs"
}

# Function to build images
build_images() {
    print_status "Building Docker images..."
    check_docker
    
    docker-compose build --no-cache
    print_success "Images built successfully!"
}

# Function to stop services
stop_services() {
    print_status "Stopping all services..."
    
    # Stop development services
    if docker-compose -f docker-compose.dev.yml ps -q > /dev/null 2>&1; then
        docker-compose -f docker-compose.dev.yml down
    fi
    
    # Stop production services
    if docker-compose --profile production ps -q > /dev/null 2>&1; then
        docker-compose --profile production down
    fi
    
    # Stop standard services
    if docker-compose ps -q > /dev/null 2>&1; then
        docker-compose down
    fi
    
    print_success "All services stopped!"
}

# Function to clean up
clean_up() {
    print_status "Cleaning up Docker containers and images..."
    
    # Stop all services first
    stop_services
    
    # Remove containers and volumes
    docker-compose down -v --remove-orphans 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down -v --remove-orphans 2>/dev/null || true
    
    # Remove images
    docker images | grep ai-debug | awk '{print $3}' | xargs -r docker rmi -f
    
    # Clean up Docker system
    docker system prune -f
    
    print_success "Cleanup completed!"
}

# Function to show logs
show_logs() {
    print_status "Showing logs from all services..."
    
    if docker-compose ps -q > /dev/null 2>&1; then
        docker-compose logs -f
    elif docker-compose -f docker-compose.dev.yml ps -q > /dev/null 2>&1; then
        docker-compose -f docker-compose.dev.yml logs -f
    else
        print_error "No running services found."
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests for all modules..."
    
    # Test Python modules
    print_status "Testing Python modules..."
    python test_prompt_refiner.py
    python test_code_analyzer.py
    python test_spec_comparer.py
    python test_debugger_engine.py
    
    # Test frontend
    print_status "Testing frontend..."
    npm run lint
    
    print_success "All tests completed!"
}

# Function to start only backend
start_backend() {
    print_status "Starting backend service only..."
    check_docker
    check_env
    
    docker-compose up --build backend
}

# Function to start only frontend
start_frontend() {
    print_status "Starting frontend service only..."
    check_docker
    
    docker-compose up --build frontend-dev
}

# Function to check health
check_health() {
    print_status "Checking service health..."
    
    # Check backend
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Backend is healthy"
    else
        print_error "Backend is not responding"
    fi
    
    # Check frontend
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "Frontend is healthy"
    else
        print_error "Frontend is not responding"
    fi
}

# Main script logic
case "${1:-help}" in
    dev)
        start_dev
        ;;
    prod)
        start_prod
        ;;
    build)
        build_images
        ;;
    stop)
        stop_services
        ;;
    clean)
        clean_up
        ;;
    logs)
        show_logs
        ;;
    test)
        run_tests
        ;;
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    health)
        check_health
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac