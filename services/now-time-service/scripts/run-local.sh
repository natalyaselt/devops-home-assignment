#!/usr/bin/env bash
#
# Runs now-time-service together with the mock /epoch service for a full
# end-to-end local test. Stops the mock automatically on exit.
#
# Usage: ./scripts/run-local.sh
set -euo pipefail

# Use JAVA_HOME if set; otherwise fall back to a JDK 21 via java_home on macOS.
# Gradle's toolchain support will otherwise locate/auto-provision Java 21.
if [[ -z "${JAVA_HOME:-}" ]] && command -v /usr/libexec/java_home >/dev/null 2>&1; then
  if JH=$(/usr/libexec/java_home -v 21 2>/dev/null); then
    export JAVA_HOME="$JH"
  fi
fi
echo "Using JAVA_HOME=${JAVA_HOME:-<system default / Gradle toolchain>}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

MOCK_PORT=8081

# Clean up any stale mock left over from a previous run that didn't exit cleanly
# (e.g. terminal closed before the EXIT trap fired), otherwise the new mock dies
# with "Address already in use".
if STALE_PIDS=$(lsof -nP -tiTCP:"$MOCK_PORT" -sTCP:LISTEN 2>/dev/null) && [[ -n "$STALE_PIDS" ]]; then
  echo "Port $MOCK_PORT already in use by PID(s): $STALE_PIDS — stopping them first."
  kill $STALE_PIDS 2>/dev/null || true
  sleep 1
fi

echo "Starting mock /epoch service on :$MOCK_PORT ..."
python3 scripts/mock_epoch_server.py &
MOCK_PID=$!
trap 'echo "Stopping mock (pid $MOCK_PID)"; kill "$MOCK_PID" 2>/dev/null || true' EXIT

# Wait until the mock is actually accepting connections before starting the app.
for _ in $(seq 1 10); do
  if lsof -nP -iTCP:"$MOCK_PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    break
  fi
  if ! kill -0 "$MOCK_PID" 2>/dev/null; then
    echo "Mock epoch service failed to start (see output above)." >&2
    exit 1
  fi
  sleep 0.5
done

GRADLE_CMD="gradle"
[[ -x ./gradlew ]] && GRADLE_CMD="./gradlew"   # prefer wrapper if present

echo "Starting now-time-service on :8080 ..."
exec "$GRADLE_CMD" bootRun
