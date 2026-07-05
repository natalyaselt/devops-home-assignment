


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

```

---

# Services

## Epoch Service (Service A)

- Technology: Python (FastAPI)
- Endpoint: POST /epoch

Request:
```json
{
  "date": "2026-06-15T10:00:00Z"
}
```
Response:
```json
{
  "epoch": 1781517600
}
```


---

## Now-Time Service (Service B)

- Technology: Java 21 (Spring Boot)
- Endpoint: GET /now

Response:
```
{
  "message": "now is 1781517600"
}
```

Behavior:
- Gets current UTC time
- Calls Epoch Service via HTTP POST /epoch
- Returns formatted response

---

# How to run

## Prerequisites
- Docker
- Docker Compose

## Start system

docker compose up --build

OR

make up

---

# Services URLs

Epoch Service:
http://localhost:8081

Now-Time Service:
http://localhost:8080

---

# Service-to-service communication

Inside Docker network:

http://epoch-service:8081/epoch

Docker Compose resolves service names automatically.

---

# Example usage

curl http://localhost:8080/now

Response:
{
  "message": "now is 1781517600"
}

---

# Architecture decisions

- Docker Compose for orchestration
- Internal Docker DNS for service discovery
- Clear separation of concerns
- Independent deployable services
- Config-driven endpoints
- Monorepo structure for simplicity

---

# Makefile (bonus)

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

---

# Optional improvements

## Healthchecks
Add healthcheck to ensure proper startup order:

healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8081/epoch"]
  interval: 10s
  retries: 5

Use:

depends_on:
  epoch-service:
    condition: service_healthy

---

## Retry logic (Spring Boot)
- Add retry for HTTP calls to epoch-service
- Use exponential backoff or Resilience4j

---

## CI pipeline (GitHub Actions)
- Run Python tests (pytest)
- Run linting (flake8/black)
- Build Java service
- Build Docker images
- Validate docker-compose build

---

# Repository structure

services/
  epoch-service/
  now-time-service/

.github/
docker-compose.yml
Makefile
README.md

---

# Summary

This project demonstrates:
- Microservices architecture
- Cross-service HTTP communication
- Dockerized local environment
- Reproducible single-command startup
- Clean DevOps structure

---

# Run everything

docker compose up --build

Then:

```
curl http://localhost:8080/now
```
Expected response(example):
```
{"message":"now is 1783231587"}

```

Call Epoch Service directly example: 
```
curl -X POST http://localhost:8081/epoch \
  -H "Content-Type: application/json" \
  -d "{\"date\":\"2026-06-15T10:00:00Z\"}"
```
Expected response:
```
{"epoch":1781517600}

```
