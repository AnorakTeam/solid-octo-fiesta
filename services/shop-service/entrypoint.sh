#!/bin/sh
set -e

echo "==> [Shop Service] Iniciando..."

if [ "$DB_ENGINE" = "postgres" ] || [ -n "$DATABASE_URL" ]; then
    echo "==> [Shop Service] Verificando conexión a PostgreSQL y asegurando base de datos..."
    python << 'EOF'
import sys
import time
import os
import psycopg

db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_PORT', '5432')
db_user = os.getenv('POSTGRES_USER', 'clicker')
db_pass = os.getenv('POSTGRES_PASSWORD', 'clicker')
db_name = os.getenv('POSTGRES_DB', 'shop_db')

database_url = os.getenv('DATABASE_URL') or os.getenv('SHOP_DATABASE_URL')
max_retries = 30
retry_interval = 2

for i in range(max_retries):
    try:
        if database_url:
            with psycopg.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            print("==> [Shop Service] Conectado exitosamente vía DATABASE_URL!")
            sys.exit(0)
        else:
            with psycopg.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pass,
                dbname='postgres',
                autocommit=True
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                    if not cur.fetchone():
                        print(f"==> [Shop Service] Base de datos '{db_name}' no existe. Creándola...")
                        cur.execute(f'CREATE DATABASE "{db_name}"')
                        print(f"==> [Shop Service] Base de datos '{db_name}' creada exitosamente.")

            with psycopg.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pass,
                dbname=db_name
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")

            print(f"==> [Shop Service] Base de datos '{db_name}' lista y verificada!")
            sys.exit(0)
    except Exception as e:
        print(f"==> [Shop Service] PostgreSQL no disponible aún ({i+1}/{max_retries}): {e}. Reintentando en {retry_interval}s...")
        time.sleep(retry_interval)

print("==> [Shop Service] ERROR: No se pudo conectar a PostgreSQL.", file=sys.stderr)
sys.exit(1)
EOF
fi

echo "==> [Shop Service] Aplicando migraciones..."
python manage.py migrate --noinput

echo "==> [Shop Service] Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "==> [Shop Service] Arrancando servidor..."
exec "$@"
