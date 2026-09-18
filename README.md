Farm Management API

REST API for managing a farm, built with FastAPI and PostgreSQL.

The application provides endpoints for managing farms, animals, fields, fieldwork, crops and financial records.

Technologies
Python 3.14
FastAPI
Pydantic
PostgreSQL 17
Psycopg 3
Docker & Docker Compose
pgAdmin
Pytest
Swagger UI

Project structure:

farm-management-app/
├── app/
│   ├── database/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   └── static/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pytest.ini
└── requirements.txt

Features

The API currently supports management of:

farms
animals
fields
fieldwork
crops
(farm) machines
financial records

The API provides CRUD operations where applicable, together with:

- request validation using Pydantic
- HTTP error handling
- PostgreSQL database integration
- automated API tests
- interactive Swagger documentation
- Configuration

Database connection settings are stored in a .env.example file.

Create .env in the root directory:

DB_HOST=postgres
DB_PORT=5432
DB_NAME=farm-management
DB_USER=postgres
DB_PASSWORD=admin

For Docker Compose, the database host should be:
.env is excluded from Git. Use .env.example as a template.

Running with Docker

Make sure Docker Desktop is running.

Build and start the application:

docker compose up --build

The services are available at:

FastAPI: http://localhost:8000
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
pgAdmin: http://localhost:1010

To stop the application:
docker compose down

Running tests

Tests can be run locally from the project's virtual environment:

pytest -v

The test suite verifies the API endpoints and their responses.

API documentation

After starting the application, interactive API documentation is available through Swagger UI:

http://localhost:8000/docs

Swagger UI allows you to view available endpoints, their parameters and request/response schemas, as well as send requests directly to the API.

Database

PostgreSQL is run as a Docker container.

The initial database structure and data are loaded from:

app/database/farm_management.sql

The PostgreSQL data is stored in a Docker volume, so it persists between container restarts.

License

This project was created as a university project.