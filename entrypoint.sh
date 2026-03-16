#!/bin/sh
set -e

# Initialize database if it doesn't exist
if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Initializing PostgreSQL database..."
    su-exec postgres initdb -D "$PGDATA"
    
    # Configure postgres to listen on localhost only
    echo "listen_addresses='127.0.0.1'" >> "$PGDATA/postgresql.conf"
    
    # Start postgres temporarily to create user and db
    su-exec postgres pg_ctl -D "$PGDATA" -w start
    
    echo "Creating netops user and database..."
    su-exec postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
        CREATE USER netops WITH PASSWORD 'netops_password';
        CREATE DATABASE netops;
        GRANT ALL PRIVILEGES ON DATABASE netops TO netops;
        \c netops
        GRANT ALL ON SCHEMA public TO netops;
EOSQL
    
    su-exec postgres pg_ctl -D "$PGDATA" -m fast -w stop
fi

# Start postgres in the background
echo "Starting PostgreSQL..."
su-exec postgres pg_ctl -D "$PGDATA" -l /var/lib/postgresql/logfile start

# Wait for postgres to be ready
echo "Waiting for PostgreSQL to be ready..."
until su-exec postgres pg_isready; do
    sleep 1
done
echo "PostgreSQL is ready."

# Start the go application
echo "Starting netops application..."
exec /app/netops
