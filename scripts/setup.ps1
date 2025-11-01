# PowerShell Setup Script for Windows
# Run this to set up the entire system

Write-Host "🚀 Hospitality Marketing Assistant - Setup Script" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
docker --version 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not installed or not running!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop/" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker is installed" -ForegroundColor Green

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env file with your API keys before continuing!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Required keys:" -ForegroundColor Cyan
    Write-Host "  - ANTHROPIC_API_KEY (get from: https://console.anthropic.com/)" -ForegroundColor White
    Write-Host ""
    Write-Host "Optional (for Instagram):" -ForegroundColor Cyan
    Write-Host "  - META_APP_ID" -ForegroundColor White
    Write-Host "  - META_APP_SECRET" -ForegroundColor White
    Write-Host "  - META_ACCESS_TOKEN" -ForegroundColor White
    Write-Host ""

    $continue = Read-Host "Have you edited .env with your keys? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Please edit .env file and run this script again." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# Stop any running containers
Write-Host ""
Write-Host "Stopping any existing containers..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null
Write-Host "✅ Cleaned up old containers" -ForegroundColor Green

# Build and start services
Write-Host ""
Write-Host "Building Docker images (this may take a few minutes)..." -ForegroundColor Yellow
docker-compose build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build complete" -ForegroundColor Green

# Start services
Write-Host ""
Write-Host "Starting services..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Services started" -ForegroundColor Green

# Wait for services to be healthy
Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
docker-compose ps

# Test database connection
Write-Host ""
Write-Host "Testing database connection..." -ForegroundColor Yellow
$dbTest = docker-compose exec -T postgres psql -U postgres -d hospitality_marketing -c "SELECT 1;" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database is ready" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database not ready yet (may need a few more seconds)" -ForegroundColor Yellow
}

# Display next steps
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✨ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your MCP marketing system is now running!" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Access Points:" -ForegroundColor Cyan
Write-Host "  • PostgreSQL: localhost:5432" -ForegroundColor White
Write-Host "  • Redis: localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Cyan
Write-Host "  • View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "  • Stop all: docker-compose down" -ForegroundColor White
Write-Host "  • Restart: docker-compose restart" -ForegroundColor White
Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Read QUICKSTART.md for testing" -ForegroundColor White
Write-Host "  2. Configure Claude Desktop to use MCP servers" -ForegroundColor White
Write-Host "  3. Start generating content!" -ForegroundColor White
Write-Host ""
Write-Host "🆘 Need help? Check README.md or open an issue" -ForegroundColor Yellow
Write-Host ""
