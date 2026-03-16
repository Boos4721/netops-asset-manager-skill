# ─── Stage 1: Build frontend ───────────────────────────────────────────────
FROM node:22-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps
COPY frontend/ ./
RUN npm run build

# ─── Stage 2: Build backend ────────────────────────────────────────────────
FROM golang:1.26-alpine AS backend
WORKDIR /app
RUN apk add --no-cache gcc musl-dev

RUN go env -w GOPROXY=https://goproxy.cn,direct

COPY go.mod go.sum ./
RUN go mod download

COPY backend/ ./backend/
# Copy built frontend into embedded path
COPY --from=frontend /app/backend/internal/embedded/dist ./backend/internal/embedded/dist

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /netops ./backend/cmd/server

# ─── Stage 3: Minimal runtime image ────────────────────────────────────────
FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata nmap openssh-client postgresql postgresql-client su-exec

WORKDIR /app
COPY --from=backend /netops ./netops
COPY config.yaml ./
COPY entrypoint.sh ./

RUN mkdir -p /app/assets /run/postgresql /var/lib/postgresql/data && \
    chown -R postgres:postgres /run/postgresql /var/lib/postgresql/data && \
    chmod +x /app/entrypoint.sh

EXPOSE 8081

ENV PORT=8081
ENV DATABASE_URL="postgres://netops:netops_password@127.0.0.1:5432/netops?sslmode=disable"
ENV JWT_SECRET="change-me"
ENV PGDATA="/var/lib/postgresql/data"

ENTRYPOINT ["/app/entrypoint.sh"]
