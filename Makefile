up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	docker compose up --build
	until curl -s http://localhost:8081/epoch -X POST \
	  -H "Content-Type: application/json" \
	  -d '{"date":"2026-06-15T10:00:00Z"}'; do sleep 1; done
	curl http://localhost:8080/now
	docker compose down