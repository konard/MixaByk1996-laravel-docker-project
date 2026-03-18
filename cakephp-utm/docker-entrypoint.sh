#!/bin/bash
set -e

: "${DB_HOST:=db}"
: "${DB_USER:=utm_user}"
: "${DB_PASS:=utm_pass}"
: "${DB_NAME:=utm_db}"

echo "Waiting for MySQL at ${DB_HOST}..."

max_tries=30
count=0
until mysqladmin ping -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" --silent 2>/dev/null; do
    count=$((count + 1))
    if [ $count -ge $max_tries ]; then
        echo "ERROR: MySQL not available after ${max_tries} attempts, exiting."
        exit 1
    fi
    echo "MySQL not ready yet (attempt ${count}/${max_tries}), waiting..."
    sleep 2
done

echo "MySQL is ready."

echo "Running database schema migration..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < /var/www/html/db/schema.sql
echo "Schema applied."

ROW_COUNT=$(mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" \
    -N -e "SELECT COUNT(*) FROM utm_data;" 2>/dev/null || echo "0")

if [ "$ROW_COUNT" = "0" ]; then
    echo "Seeding database..."
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < /var/www/html/db/seed.sql
    echo "Seed data applied."
else
    echo "Database already has ${ROW_COUNT} rows, skipping seed."
fi

echo "Starting Apache..."
exec apache2-foreground
