# ─── Stage 1: Build frontend ───────────────────────────────────────────────
FROM node:22-alpine AS frontend
WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci --legacy-peer-deps
COPY web/ ./
RUN npm run build

# ─── Stage 2: Build backend ────────────────────────────────────────────────
FROM golang:1.26-alpine AS backend
WORKDIR /app
# Install C compiler for cgo deps (if any)
RUN apk add --no-cache gcc musl-dev

COPY go.mod go.sum ./
RUN go mod download

COPY . .
# Copy built frontend into embedded path
COPY --from=frontend /app/internal/embedded/dist ./internal/embedded/dist

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /netops ./cmd/server

# ─── Stage 3: Minimal runtime image ────────────────────────────────────────
FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata nmap openssh-client

WORKDIR /app
COPY --from=backend /netops ./netops
COPY config.yaml ./

# Create assets directory for JSON backups
RUN mkdir -p /app/assets

EXPOSE 8081

ENV PORT=8081
ENV DATABASE_URL=""
ENV JWT_SECRET="change-me"

ENTRYPOINT ["/app/netops"]
