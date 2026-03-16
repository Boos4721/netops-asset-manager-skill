BINARY    := netops
WEB_DIR   := web
DIST_DIR  := internal/embedded/dist
SERVER    := ./cmd/server
MIGRATE   := ./cmd/migrate

.PHONY: all build build-frontend build-backend migrate dev-frontend dev-backend clean docker-build docker-run

all: build

## Build frontend then backend into single binary
build: build-frontend build-backend

build-frontend:
	@echo "==> Building frontend..."
	cd $(WEB_DIR) && npm run build

build-backend:
	@echo "==> Building backend..."
	go build -ldflags="-s -w" -o $(BINARY) $(SERVER)

## Run data migration (inventory.json → PostgreSQL)
migrate:
	go run $(MIGRATE)

## Development servers (run in separate terminals)
dev-frontend:
	cd $(WEB_DIR) && npm run dev

dev-backend:
	@command -v air >/dev/null 2>&1 && air || go run $(SERVER)

## Tidy Go modules
tidy:
	go mod tidy

## Re-generate Ent schema code
generate:
	go run entgo.io/ent/cmd/ent generate ./ent/schema

## Clean build artifacts
clean:
	rm -f $(BINARY)
	rm -rf $(DIST_DIR)

## Docker build
docker-build: build
	docker build -t netops-asset-manager:latest .

## Docker run
docker-run:
	docker run -p 8081:8081 \
		-e DATABASE_URL="$$DATABASE_URL" \
		-e JWT_SECRET="$$JWT_SECRET" \
		netops-asset-manager:latest

## Install Go tooling
install-tools:
	go install github.com/air-verse/air@latest
