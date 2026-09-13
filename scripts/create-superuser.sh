#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT_DIR}"

echo "👤 Creando superusuario en identity-service dentro del contenedor (con sudo)..."
sudo docker compose exec identity-service python manage.py createsuperuser
