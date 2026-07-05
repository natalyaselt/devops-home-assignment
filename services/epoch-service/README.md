# Epoch Service

## Overview

Epoch Service is a simple REST API that receives a date in ISO-8601 format and returns the corresponding Unix Epoch timestamp.

---

## Project Structure

```
app/
    main.py         Application entry point
    routes.py       REST API endpoints
    models.py       Request/response models
    config.py       Configuration loader

config/
    config.yaml     Application configuration

tests/
    test_epoch.py   Unit tests
```

---

## Requirements

- Python 3.12+
- pip

---

## Installation

Clone the repository.

Install dependencies.

```bash
pip install -r requirements.txt
```
Code formatting (Black)
```
python -m black app tests
```
Linting (Flake8) checks:
- unused imports
- style issues
- missing whitespace rules
- code complexity issues
```
python -m flake8 app
```

---

## Configuration

Application settings are stored in

```
config/config.yaml
```

Example:

```yaml
server:
  host: 0.0.0.0
  port: 8080

api:
  epoch_endpoint: /epoch
```

---

## Running the service

### Command line

```bash
python -m app.main
```
The service starts on the configured host and port.

---

## Using the service

POST

```
http://localhost:8080/epoch
```

Request

```json
{
    "date": "2026-06-15T10:00:00Z"
}
```

Successful response

```json
{
    "epoch": 1781517600
}
```

## Request example using curl

Request
```
curl -i -X POST http://localhost:8080/epoch \
  -H "Content-Type: application/json" \
  -d "{\"date\":\"2026-06-15T11:00:00Z\"}"
```
Expected response:
```
HTTP/1.1 200 OK
{
    "epoch":1781517600
}
```

---

## Error Handling

| Status | Description |
|---------|-------------|
|200|Successful request|
|400|Malformed request|
|422|Invalid date format|
|500|Unexpected server error|

---

## Running Tests
From the project root:
```bash
python -m pytest
```

---

## Continuous Integration

GitHub Actions automatically:

- installs dependencies
- runs unit tests
- fails the build if any test fails
