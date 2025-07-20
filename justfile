# Default recipe to display help
default:
    @just --list

# Setup and Development Commands
setup: install-deps install-pre-commit build create-env up migrate superuser
    @echo "🎉 Project setup complete!"
    @echo "Development server is now running at http://localhost:8000"

# Install dependencies
install-deps:
    @echo "📦 Installing dependencies..."
    uv sync --all-extras

# Install pre-commit hooks
install-pre-commit:
    @echo "🔧 Installing pre-commit hooks..."
    uv run pre-commit install

# Build Docker containers
build:
    @echo "🐳 Building Docker containers..."
    docker-compose build

# Create .env file from example
create-env:
    @echo "⚙️  Creating .env file..."
    cp .env.example .env
    @echo "⚙️  Creating pgAdmin servers configuration..."
    cp pgadmin-servers.json.example pgadmin-servers.json
    @echo "Please update .env file with your specific values"

# Docker Management Commands
up:
    @echo "🚀 Starting development server..."
    docker-compose up -d

down:
    @echo "🛑 Stopping containers..."
    docker-compose down

restart: down up
    @echo "🔄 Containers restarted"

logs service="web":
    @echo "📋 Showing logs for {{service}}..."
    docker-compose logs -f {{service}}

# Database Commands
migrate:
    @echo "🗃️  Running migrations..."
    docker-compose exec web .venv/bin/python manage.py migrate

makemigrations app="":
    @echo "📝 Creating migrations..."
    docker-compose exec web .venv/bin/python manage.py makemigrations {{app}}

superuser:
    @echo "👤 Creating superuser..."
    docker-compose exec web .venv/bin/python manage.py createsuperuser

dbshell:
    @echo "💾 Opening database shell..."
    docker-compose exec web .venv/bin/python manage.py dbshell

# Django Management Commands
shell:
    @echo "🐍 Opening Django shell..."
    docker-compose exec web .venv/bin/python manage.py shell_plus

collectstatic:
    @echo "📁 Collecting static files..."
    docker-compose exec web .venv/bin/python manage.py collectstatic --noinput

check:
    @echo "✅ Running Django checks..."
    docker-compose exec web .venv/bin/python manage.py check

# Testing Commands
test:
    @echo "🧪 Running tests..."
    docker-compose exec web uv run pytest

test-cov:
    @echo "📊 Running tests with coverage..."
    docker-compose exec web uv run pytest --cov=. --cov-report=html --cov-report=term-missing

test-file file:
    @echo "🎯 Running specific test file: {{file}}"
    docker-compose exec web uv run pytest {{file}}

# Code Quality Commands
lint:
    @echo "🔍 Running linting..."
    docker-compose exec web uv run ruff check .

lint-fix:
    @echo "🔧 Running linting with auto-fix..."
    docker-compose exec web uv run ruff check --fix .

format:
    @echo "🎨 Formatting code..."
    docker-compose exec web uv run black .

typecheck:
    @echo "📝 Running type checks..."
    docker-compose exec web uv run mypy .

pre-commit:
    @echo "🔄 Running pre-commit hooks..."
    docker-compose exec web uv run pre-commit run --all-files

# Quality check all at once
quality: lint typecheck test
    @echo "✨ All quality checks passed!"

# Development Utilities
clean:
    @echo "🧹 Cleaning up..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f

reset-db: down
    @echo "🗑️  Resetting database..."
    docker volume rm core_postgres_data || true
    just up
    sleep 5
    just migrate
    just superuser

# Production Commands
prod-build:
    @echo "🏭 Building production image..."
    docker build -t core:latest .

prod-deploy:
    @echo "🚀 Deploying to production..."
    docker-compose -f docker-compose.prod.yml up -d

# Backup Commands
backup-db:
    @echo "💾 Creating database backup..."
    docker-compose exec db pg_dump -U $(DATABASE_USER) $(DATABASE_NAME) > backup_$(date +%Y%m%d_%H%M%S).sql

restore-db file:
    @echo "📥 Restoring database from {{file}}..."
    docker-compose exec -T db psql -U $(DATABASE_USER) $(DATABASE_NAME) < {{file}}

# Security Commands
security-check:
    @echo "🔒 Running security checks..."
    docker-compose exec web .venv/bin/python manage.py check --deploy

# Monitoring Commands
health:
    @echo "🏥 Checking service health..."
    curl -f http://localhost:8000/health/ || echo "❌ Web service is down"
    docker-compose exec db pg_isready -U $(DATABASE_USER) -d $(DATABASE_NAME) && echo "✅ Database is healthy" || echo "❌ Database is down"

# Admin Tools
pgadmin:
    @echo "🗄️  Opening pgAdmin..."
    @echo "URL: http://localhost:5050"
    @echo "Email: admin@example.com"
    @echo "Password: admin123"
    @echo ""
    @echo "Database connection is pre-configured as 'Django Core Database'"
    @echo "Database password: core_password"

# Update Commands
update-deps:
    @echo "⬆️  Updating dependencies..."
    uv lock --upgrade

# Generate secret key
generate-secret:
    @echo "🔑 Generating new SECRET_KEY..."
    docker-compose exec web .venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
