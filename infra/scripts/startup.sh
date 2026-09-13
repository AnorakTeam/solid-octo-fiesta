#!/bin/bash
set -euxo pipefail

exec > >(tee -a /var/log/startup-app.log) 2>&1

echo "========================================================="
echo "   Iniciando Aprovisionamiento Completo en GCP VM        "
echo "========================================================="

# 1. Configurar memoria Swap de 2GB (esencial para estabilidad en VMs económicas e2-small/medium)
if [ ! -f /swapfile ]; then
    echo "⚙️ Configurando archivo Swap de 2GB..."
    fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    sysctl vm.swappiness=10
    echo 'vm.swappiness=10' >> /etc/sysctl.conf
fi

# 2. Actualizar repositorios e instalar utilidades esenciales
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    htop \
    ufw \
    net-tools

# 3. Instalar Docker CE y Docker Compose Plugin oficial
if ! command -v docker &> /dev/null; then
    echo "🐳 Instalando Docker Engine y plugins..."
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

systemctl enable docker
systemctl start docker

# 4. Configurar permisos para usuarios locales
for u in ubuntu $(ls /home 2>/dev/null || true); do
    if id "$u" &>/dev/null; then
        usermod -aG docker "$u" || true
    fi
done

# 5. Clonar o actualizar el repositorio del proyecto
APP_DIR="/opt/solid-octo-fiesta"
GIT_REPO="${git_repo_url}"
GIT_BRANCH="${git_branch}"

echo "📦 Clonando código desde $GIT_REPO (rama: $GIT_BRANCH)..."
if [ ! -d "$APP_DIR/.git" ]; then
    mkdir -p "$APP_DIR"
    git clone -b "$GIT_BRANCH" "$GIT_REPO" "$APP_DIR"
else
    cd "$APP_DIR"
    git pull origin "$GIT_BRANCH" || true
fi

# 6. Permisos completos para evitar errores de 'Permission denied' al interactuar
chmod -R 777 "$APP_DIR" || true

# 7. Configurar variables de entorno iniciales
cd "$APP_DIR"
if [ ! -f .env ]; then
    echo "📝 Generando archivo .env principal..."
    cp .env.example .env
fi

# Asegurar que NUXT_PUBLIC_API_BASE use el proxy /api/v1 (cero errores de CORS)
sed -i 's|NUXT_PUBLIC_API_BASE=.*|NUXT_PUBLIC_API_BASE=/api/v1|' .env

# 8. Ejecutar script de arranque de microservicios
echo "🚀 Levantando microservicios, bases de datos y frontend..."
bash scripts/start-local.sh

echo "========================================================="
echo "   🎉 Aprovisionamiento y Despliegue Completado al 100%"
echo "========================================================="
touch "$APP_DIR/DEPLOY_READY"
