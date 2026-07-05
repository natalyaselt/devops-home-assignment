# DevOps Home Assignment – Monorepo (Epoch + Now-Time Service)

This repository contains a two-service system demonstrating REST APIs, service-to-service communication, Docker-based orchestration, and a reproducible local development environment.

---

# Architecture

```

User
|
v
GET /now
(now-time-service - Spring Boot)
|
v
POST /epoch
(epoch-service - FastAPI)
|
v
Unix epoch response
|
v
"now is <epoch>"

````

---

# Services

## Epoch Service (Service A)

- Technology: Python (FastAPI)
- Endpoint: POST /epoch

### Request
```json
{
  "date": "2026-06-15T10:00:00Z"
}
````

### Response

```json
{
  "epoch": 1781517600
}
```

---

## Now-Time Service (Service B)

* Technology: Java 21 (Spring Boot)
* Endpoint: GET /now

### Response

```json
{
  "message": "now is 1781517600"
}
```

### Behavior

* Gets current UTC time
* Calls Epoch Service via HTTP POST /epoch
* Returns formatted response

---

# How to run

## Prerequisites

* Docker
* Docker Compose

## Start system

```bash
docker compose up --build
```

OR

```bash
make up
```

---

# Services URLs

* Epoch Service: [http://localhost:8081](http://localhost:8081)
* Now-Time Service: [http://localhost:8080](http://localhost:8080)

---

# Service-to-service communication

Inside Docker network:

```
http://epoch-service:8081/epoch
```

Docker Compose handles service discovery automatically.

---

# Example usage

```bash
curl http://localhost:8080/now
```

Response:

```json
{"message":"now is 1781517600"}
```

---

# Repository structure

```
services/
  epoch-service/
  now-time-service/

.github/
docker-compose.yml
Makefile
README.md
```

---

# Makefile (bonus)

```makefile
up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f
```

---

# CI Pipeline (GitHub Actions)

The CI pipeline runs automatically on GitHub.

## Pull Request pipeline

Runs on every PR:

* Python formatting check (black)
* Python linting (flake8)
* Python tests (pytest)
* Java build (Gradle)
* Docker build validation

## Main branch pipeline

Runs on push to `main`:

* Build Docker images:

  * epoch-service
  * now-time-service
* Generate image tags (commit SHA)
* Simulate container registry publishing (no real push required)

---

## How to run CI locally

### Epoch Service

```bash
cd services/epoch-service
python -m black --check app tests
python -m flake8 app
python -m pytest
```

### Now-Time Service

```bash
cd services/now-time-service
./gradlew build
```

### Full system integration

```bash
docker compose up --build
curl http://localhost:8080/now
```

---

# Design decisions & assumptions

## Architecture decisions

* FastAPI used for lightweight Epoch Service
* Spring Boot used for Now-Time Service
* Docker Compose used for local orchestration
* Monorepo structure for simplicity and CI integration

## Service communication

* Internal Docker DNS used:

```
http://epoch-service:8081/epoch
```

## Reliability

* Healthcheck ensures Epoch Service readiness
* depends_on with service_healthy used to avoid race conditions
* Connection timeout configured in Java client

## CI strategy

* Separate jobs for Python, Java, Docker, and integration tests
* Integration tests validate real service-to-service HTTP calls

## Assumptions

* No production deployment required
* No real container registry push required
* Local Docker environment is the source of truth

---

# Failure handling (important)

If Epoch Service is unavailable:

* Now-Time Service may fail the request
* Or return a controlled error depending on configuration

Healthchecks ensure service startup order in Docker Compose.

---

# Production improvements (not implemented)

* Kubernetes deployment instead of Docker Compose
* Distributed tracing (OpenTelemetry)
* Circuit breaker + retry (Resilience4j)
* Real container registry (GHCR / ECR)
* Observability stack (Prometheus + Grafana)
* Improved retry strategy in service communication

---

# One-command run

```bash
docker compose up --build
```

Then:

```bash
curl http://localhost:8080/now
```

---

# What is included

✔ Epoch Service (Python FastAPI)
✔ Now-Time Service (Java Spring Boot)
✔ Docker Compose orchestration
✔ CI pipeline (GitHub Actions)
✔ Integration tests
✔ Health checks
✔ Service-to-service communication
✔ Clean documentation

---

# Summary

This project demonstrates:

* Microservices architecture
* Cross-service HTTP communication
* Dockerized development environment
* CI/CD pipeline design
* Integration testing strategy

---

