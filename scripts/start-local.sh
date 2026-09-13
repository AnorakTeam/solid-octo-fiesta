#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT_DIR}"

echo "========================================================"
echo "   Iniciando Arquitectura de Microservicios Docker"
echo "========================================================"

# Verificar docker
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado en el sistema."
    exit 1
fi

# Preparar archivo .env principal si no existe
if [ ! -f .env ]; then
    echo "ℹ️  No se encontró .env en la raíz. Creando desde .env.example..."
    cp .env.example .env
fi

# Preparar archivos .env para cada microservicio si no existen
for svc in identity-service game-service shop-service leaderboard-service; do
    if [ ! -f "services/$svc/.env" ] && [ -f "services/$svc/.env.example" ]; then
        echo "ℹ️  Creando services/$svc/.env..."
        cp "services/$svc/.env.example" "services/$svc/.env"
    fi
done

# Preparar archivo .env en frontend si no existe
if [ ! -f frontend/.env ]; then
    echo "ℹ️  No se encontró frontend/.env. Creando desde frontend/.env.dev..."
    cp frontend/.env.dev frontend/.env
fi

echo "🚀 Asegurando servicios de infraestructura (PostgreSQL y Redis)..."
sudo docker compose up -d db redis

echo "⏳ Esperando a que PostgreSQL esté listo para aceptar conexiones..."
until sudo docker compose exec -T db pg_isready -U clicker > /dev/null 2>&1; do
    sleep 1
done

echo "🗄️  Asegurando bases de datos independientes..."
for dbname in identity_db game_db shop_db leaderboard_db; do
    sudo docker compose exec -T db psql -U clicker -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$dbname'" | grep -q 1 || \
    sudo docker compose exec -T db psql -U clicker -d postgres -c "CREATE DATABASE $dbname;" || true
done

echo "📦 Construyendo y levantando todos los microservicios en segundo plano..."
sudo docker compose up --build -d

echo ""
echo "⏳ Esperando a que los servicios estén inicializados..."
sleep 5

sudo docker compose ps

echo ""
echo "========================================================"
echo "   🎉 ¡Microservicios listos y en ejecución!"
echo "========================================================"
echo "   🕹️  Frontend (Nuxt):          http://localhost:3000"
echo "   🚪  API Gateway (Nginx):      http://localhost:8000/api/v1/health"
echo "   🔑  Identity Service:         http://localhost:8001"
echo "   🎮  Game Progress Service:    http://localhost:8002"
echo "   🛒  Shop / Upgrades Service:  http://localhost:8003"
echo "   🏆  Leaderboard Service:      http://localhost:8004"
echo "   🗄️  PostgreSQL:               localhost:5432"
echo "   ⚡  Redis Event Bus:          localhost:6379"
echo ""
echo " Comandos útiles:"
echo "   - Ver logs globales:          sudo docker compose logs -f"
echo "   - Ver logs del gateway:       sudo docker compose logs -f gateway"
echo "   - Ver logs de identidad:      sudo docker compose logs -f identity-service"
echo "   - Ver logs del juego:         sudo docker compose logs -f game-service"
echo "   - Ver logs de la tienda:      sudo docker compose logs -f shop-service"
echo "   - Ver logs del leaderboard:   sudo docker compose logs -f leaderboard-service"
echo "   - Crear superusuario:         bash scripts/create-superuser.sh"
echo "   - Detener todo:               bash scripts/stop-local.sh"
echo "========================================================"
