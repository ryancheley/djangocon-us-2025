# Core - Django Healthcare Application

A Django 5.2 application built with 12-factor app principles, using PostgreSQL 17 as the database and including pgAdmin for database administration.

## Features

- Django 5.2 with Python 3.13
- PostgreSQL 17 database
- pgAdmin 4 for database administration
- Docker containerization
- 12-factor app compliance with django-environ
- Comprehensive testing setup with pytest
- Code quality tools (Black, Ruff, mypy)
- Pre-commit hooks
- Health check endpoint
- Just command runner for streamlined workflow

## Prerequisites

- Docker and Docker Compose
- Just command runner (`brew install just` on macOS)
- Python 3.13+ (for local development)
- uv package manager

## Quick Start

1. Clone the repository and navigate to the project:

   ```bash
   cd core
   ```

2. Run the complete setup:

   ```bash
   just setup
   ```

3. Start the development server:

   ```bash
   just up
   ```

4. Access the services:

   - Django application: <http://localhost:8000>
   - pgAdmin: <http://localhost:5050> (<admin@core.local> / admin123)
   - Health check: <http://localhost:8000/health/>

## Available Commands

Run `just --list` to see all available commands. Here are the most common ones:

### Development
- `just up` - Start all services
- `just down` - Stop all services
- `just restart` - Restart all services
- `just logs` - View logs

### Database
- `just migrate` - Run migrations
- `just makemigrations` - Create new migrations
- `just superuser` - Create superuser
- `just dbshell` - Open database shell
- `just pgadmin` - Show pgAdmin access info

### Testing & Quality
- `just test` - Run tests
- `just test-cov` - Run tests with coverage
- `just lint` - Check code with ruff
- `just format` - Format code with black
- `just typecheck` - Run type checking
- `just quality` - Run all quality checks

### Utilities
- `just shell` - Django shell with extensions
- `just clean` - Clean up containers
- `just reset-db` - Reset database (destructive!)


## Environment Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Key environment variables:
- `SECRET_KEY` - Django secret key (generate with `just generate-secret`)
- `DEBUG` - Debug mode (True/False)
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Development Workflow

1. Make changes to the code
2. Run quality checks: `just quality`
3. Fix any issues: `just lint-fix` and `just format`
4. Run tests: `just test`
5. Commit changes (pre-commit hooks will run automatically)

## Testing

The project uses pytest for testing with coverage reporting:

```bash
just test         # Run all tests
just test-cov     # Run with coverage report
just test-file apps/accounts/tests.py  # Run specific test file
```

## Code Quality

The project enforces code quality through:
- **Black** - Code formatting
- **Ruff** - Fast Python linting
- **mypy** - Static type checking
- **pre-commit** - Git hooks for automated checks

## Database Management

- PostgreSQL 17 is used as the primary database
- pgAdmin 4 is included for database administration
- Migrations are managed through Django's migration system
- Database backups: `just backup-db`
- Database restore: `just restore-db backup.sql`

## Security

- Environment-based configuration
- Secure session and CSRF cookies
- HTTPS enforcement in production
- Security headers configured
- Regular security checks: `just security-check`
