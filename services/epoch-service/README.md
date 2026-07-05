# Epoch Service

## Overview

Epoch Service is a lightweight REST API built with FastAPI.  
It receives an ISO-8601 formatted date and returns the corresponding Unix epoch timestamp.

---

## Base URL (Docker)

```

[http://localhost:8081](http://localhost:8081)

```

> In Docker Compose, this service is reachable internally as:
> `http://epoch-service:8081`

---

## Endpoint

### Convert Date to Epoch

```

POST /epoch

````

---

## Request

```json
{
  "date": "2026-06-15T10:00:00Z"
}
````

* `date` must be a valid ISO-8601 UTC timestamp
* Required field

---

## Response

```json
{
  "epoch": 1781517600
}
```

---

## Error Responses

| Status Code | Meaning                                          |
| ----------- | ------------------------------------------------ |
| 200         | Success                                          |
| 405         | Method not allowed (e.g., GET instead of POST)   |
| 422         | Validation error (invalid or missing date field) |
| 500         | Internal server error                            |

---

## Configuration

Service configuration is defined in:

```
config/config.yaml
```

Example:

```yaml
server:
  host: 0.0.0.0
  port: 8081

api:
  epoch_endpoint: /epoch
```

### Notes

* `host: 0.0.0.0` is required for Docker networking
* Port may be overridden in Docker Compose

---

## Running Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start service

```bash
python -m app.main
```

Service will start on:

```
http://localhost:8080
```

---

## Running with Docker (Recommended)

From the monorepo root:

```bash
docker compose up --build
```

---

## Example Usage (curl)

```bash
curl -X POST http://localhost:8081/epoch \
  -H "Content-Type: application/json" \
  -d "{\"date\":\"2026-06-15T10:00:00Z\"}"
```

---

## Testing

Run unit tests:

```bash
python -m pytest
```

---

## Code Quality Tools

### Black (formatter)

Ensures consistent code formatting:

```bash
python -m black app tests
```

### Flake8 (linter)

Checks:

* style issues
* unused imports
* code complexity
* PEP8 violations

```bash
python -m flake8 app
```

---

## Notes

* This service is stateless
* Designed for microservice integration
* Used by `now-time-service` via HTTP call
* Docker Compose is the recommended execution environment

```
