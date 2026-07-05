# now-time-service

A small Spring Boot service exposing a single **GET** endpoint. On each call it:

1. Takes the current time (`Instant.now()` in UTC).
2. Calls an external `POST /epoch` service with that timestamp.
3. Wraps the returned epoch as a friendly message: `now is <epoch>`.

## Endpoint

```
GET /now
```

Example response:

```json
{ "message": "now is 1781517600" }
```

### How it talks to the external service

It sends:

```
POST {epoch.base-url}/epoch
Content-Type: application/json

{ "date": "2026-06-15T10:00:00Z" }
```

and expects:

```json
{ "epoch": 1781517600 }
```

## Requirements

- **Java 21** (Spring Boot 3.5.x runs on Java 17–24; this project targets 21).
  If you don't have JDK 21 installed, Gradle will download it automatically via the
  toolchain resolver — you just need an internet connection.
- **Gradle 8.14+ or 9.x** (or use the wrapper — see below).
- **Python 3** — only for the bundled mock `/epoch` service used in local testing.
- **Internet access** — dependencies are fetched from Maven Central and the Gradle
  Plugin Portal on the first build, then cached locally.

## Quick start (with the bundled mock /epoch service)

This is the fastest way to see it work end-to-end. The script starts the mock
`/epoch` service on port 8081, then the app on port 8080, and stops the mock
automatically when you exit.

```bash
cd now-time-service
./scripts/run-local.sh
```

Wait for `Started NowTimeServiceApplication`, then in another terminal:

```bash
curl http://localhost:8080/now
```

Expected response (the number is the current epoch seconds):

```json
{ "message": "now is 1782049513" }
```

Press `Ctrl+C` in the `run-local.sh` terminal to stop both processes.

## Running manually

Start the app on its own (it will call whatever `/epoch` service `EPOCH_BASEURL`
points at):

```bash
cd now-time-service
gradle bootRun
```

In a separate terminal you can run the bundled mock if you don't have a real
`/epoch` service:

```bash
python3 scripts/mock_epoch_server.py
```

### Run against a real /epoch service

```bash
EPOCH_BASEURL=https://your-epoch-host gradle bootRun
```

## Using the Gradle wrapper (no Gradle install needed)

If you don't have Gradle installed, generate the wrapper once (requires Gradle on
your `PATH` for this single step), then use `./gradlew` everywhere afterwards:

```bash
gradle wrapper --gradle-version 9.6
./gradlew bootRun
```

## Configuration

| Property         | Env var         | Default                 | Description                            |
| ---------------- | --------------- | ----------------------- | -------------------------------------- |
| `epoch.base-url` | `EPOCH_BASEURL` | `http://localhost:8081` | Base URL of the external epoch service |
| `server.port`    | `SERVER_PORT`   | `8080`                  | Port this service listens on           |

Example overriding the port:

```bash
SERVER_PORT=9090 EPOCH_BASEURL=http://localhost:8081 gradle bootRun
```

## Test

```bash
gradle test
```

## Project layout

```
build.gradle                      Spring Boot 3.5.6, Java 21 toolchain, BOM-based deps
settings.gradle                   Project name + JDK toolchain auto-provisioning
src/main/java/com/example/nowtime
  NowTimeServiceApplication.java  Spring Boot entry point
  NowController.java              GET /now endpoint
  EpochClient.java                Calls POST /epoch via RestClient
  EpochClientConfig.java          RestClient bean (base URL, timeouts)
  EpochRequest.java               { "date": ... } request DTO
  EpochResponse.java              { "epoch": ... } response DTO
  NowResponse.java                { "message": ... } response DTO
scripts/
  mock_epoch_server.py            Dependency-free mock of the external /epoch API
  run-local.sh                    Runs the mock + the app together
```

## Troubleshooting

- **First build is slow** — it's downloading dependencies from Maven Central; they're
  cached afterwards.
- **`Port 8080 was already in use`** — another process holds the port. Stop it, or
  run with `SERVER_PORT=9090 gradle bootRun`.
- **`bootRun` appears stuck around 80%** — this is normal; Spring Boot apps keep the
  Gradle task running while the server is up. Hit the endpoint or `Ctrl+C` to stop.
- **`GET /now` returns 500** — the external `/epoch` service isn't reachable. Use
  `./scripts/run-local.sh` (starts the mock) or set `EPOCH_BASEURL` to a live service.
