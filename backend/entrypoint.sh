#!/bin/sh
set -e

echo "==> Iniciando backend solid-octo-fiesta..."

# Esperar a que la base de datos esté lista si se usa PostgreSQL
if [ "$DB_ENGINE" = "postgres" ] || [ -n "$DATABASE_URL" ]; then
    echo "==> Verificando conexión con la base de datos..."
    python << 'EOF'
import sys
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.db import connections
from django.db.utils import OperationalError

db_conn = connections['default']
max_retries = 30
retry_interval = 2

for i in range(max_retries):
    try:
        db_conn.cursor()
        print("==> ¡Base de datos conectada exitosamente!")
        sys.exit(0)
    except OperationalError as e:
        print(f"==> Base de datos no disponible aún ({i+1}/{max_retries}). Reintentando en {retry_interval}s...")
        time.sleep(retry_interval)

print("==> ERROR: No se pudo conectar a la base de datos tras varios intentos.", file=sys.stderr)
sys.exit(1)
EOF
fi

echo "==> Aplicando migraciones de base de datos..."
python manage.py migrate --noinput

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Ejecutando comando del servidor..."
exec "$@"
