# Default recipe to display help
default:
    @just --list --list-submodules

# Complete project setup
[group: 'setup']
setup: install-deps install-pre-commit build create-env up migrate superuser
    @echo "🎉 Project setup complete!"
    @echo "Development server is now running at http://localhost:8000"

# Install dependencies
[group: 'setup']
install-deps:
    @echo "📦 Installing dependencies..."
    uv sync --all-extras

# Install pre-commit hooks
[group: 'setup']
install-pre-commit:
    @echo "🔧 Installing pre-commit hooks..."
    uv run pre-commit install

# Create .env file from example
[group: 'setup']
create-env:
    @echo "⚙️  Creating .env file..."
    cp .env.example .env
    @echo "⚙️  Creating pgAdmin servers configuration..."
    cp pgadmin-servers.json.example pgadmin-servers.json
    @echo "Please update .env file with your specific values"

# Build Docker containers
[group: 'docker']
build:
    @echo "🐳 Building Docker containers..."
    docker-compose build

# Start development server
[group: 'docker']
up:
    @echo "🚀 Starting development server..."
    docker-compose up -d

# Stop containers
[group: 'docker']
down:
    @echo "🛑 Stopping containers..."
    docker-compose down

# Restart containers
[group: 'docker']
restart: down up
    @echo "🔄 Containers restarted"

# Show container logs
[group: 'docker']
logs service="web":
    @echo "📋 Showing logs for {{service}}..."
    docker-compose logs -f {{service}}

# Run Django migrations
[group: 'database']
migrate:
    @echo "🗃️  Running migrations..."
    docker-compose exec web .venv/bin/python manage.py migrate

# Create Django migrations
[group: 'database']
makemigrations app="":
    @echo "📝 Creating migrations..."
    docker-compose exec web .venv/bin/python manage.py makemigrations {{app}}

# Create Django superuser
[group: 'database']
superuser:
    @echo "👤 Creating superuser..."
    docker-compose exec web .venv/bin/python manage.py createsuperuser

# Open database shell
[group: 'database']
dbshell:
    @echo "💾 Opening database shell..."
    docker-compose exec web .venv/bin/python manage.py dbshell

# Reset database
[group: 'database']
reset-db: down
    @echo "🗑️  Resetting database..."
    docker volume rm core_postgres_data || true
    just up
    sleep 5
    just migrate
    just superuser

# Create database backup
[group: 'database']
backup-db:
    @echo "💾 Creating database backup..."
    docker-compose exec db pg_dump -U $(DATABASE_USER) $(DATABASE_NAME) > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database from backup
[group: 'database']
restore-db file:
    @echo "📥 Restoring database from {{file}}..."
    docker-compose exec -T db psql -U $(DATABASE_USER) $(DATABASE_NAME) < {{file}}

# Open Django shell
[group: 'django']
shell:
    @echo "🐍 Opening Django shell..."
    docker-compose exec web .venv/bin/python manage.py shell_plus

# Collect static files
[group: 'django']
collectstatic:
    @echo "📁 Collecting static files..."
    docker-compose exec web .venv/bin/python manage.py collectstatic --noinput

# Run Django system checks
[group: 'django']
check:
    @echo "✅ Running Django checks..."
    docker-compose exec web .venv/bin/python manage.py check

# Generate new SECRET_KEY
[group: 'django']
generate-secret:
    @echo "🔑 Generating new SECRET_KEY..."
    docker-compose exec web .venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Run all tests
[group: 'testing']
test:
    @echo "🧪 Running tests..."
    docker-compose exec web uv run pytest

# Run tests with coverage
[group: 'testing']
test-cov:
    @echo "📊 Running tests with coverage..."
    docker-compose exec web uv run pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
[group: 'testing']
test-file file:
    @echo "🎯 Running specific test file: {{file}}"
    docker-compose exec web uv run pytest {{file}}

# Run linting
[group: 'quality']
lint:
    @echo "🔍 Running linting..."
    docker-compose exec web uv run ruff check .

# Run linting with auto-fix
[group: 'quality']
lint-fix:
    @echo "🔧 Running linting with auto-fix..."
    docker-compose exec web uv run ruff check --fix .

# Format code
[group: 'quality']
format:
    @echo "🎨 Formatting code..."
    docker-compose exec web uv run ruff format .

# Run type checks
[group: 'quality']
typecheck:
    @echo "📝 Running type checks..."
    docker-compose exec web uv run ty check

# Run pre-commit hooks
[group: 'quality']
pre-commit:
    @echo "🔄 Running pre-commit hooks..."
    docker-compose exec web uv run pre-commit run --all-files

# Run all quality checks
[group: 'quality']
quality: lint typecheck test
    @echo "✨ All quality checks passed!"

# Clean up containers and volumes
[group: 'utilities']
clean:
    @echo "🧹 Cleaning up..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f

# Update dependencies
[group: 'utilities']
update-deps:
    @echo "⬆️  Updating dependencies..."
    uv lock --upgrade

# Build production image
[group: 'production']
prod-build:
    @echo "🏭 Building production image..."
    docker build -t core:latest .

# Deploy to production
[group: 'production']
prod-deploy:
    @echo "🚀 Deploying to production..."
    docker-compose -f docker-compose.prod.yml up -d

# Run security checks
[group: 'monitoring']
security-check:
    @echo "🔒 Running security checks..."
    docker-compose exec web .venv/bin/python manage.py check --deploy

# Check service health
[group: 'monitoring']
health:
    @echo "🏥 Checking service health..."
    curl -f http://localhost:8000/health/ || echo "❌ Web service is down"
    docker-compose exec db pg_isready -U $(DATABASE_USER) -d $(DATABASE_NAME) && echo "✅ Database is healthy" || echo "❌ Database is down"

# Show pgAdmin connection info
[group: 'admin']
pgadmin:
    @echo "🗄️  Opening pgAdmin..."
    @echo "URL: http://localhost:5050"
    @echo "Email: admin@example.com"
    @echo "Password: admin123"
    @echo ""
    @echo "Database connection is pre-configured as 'Django Core Database'"
    @echo "Database password: core_password"
