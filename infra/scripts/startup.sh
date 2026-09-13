#!/bin/bash
set -euxo pipefail

echo "========================================================="
echo "   Iniciando aprovisionamiento de VM para Microservicios "
echo "========================================================="

# 1. Configurar memoria Swap de 2GB (esencial para estabilidad en VMs de bajo costo e2-small/medium)
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

# 2. Actualizar repositorios e instalar utilidades básicas
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
    echo "🐳 Instalando Docker Engine..."
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

# 4. Configurar permisos de usuario para Docker
for u in ubuntu $(ls /home); do
    if id "$u" &>/dev/null; then
        usermod -aG docker "$u" || true
    fi
done

# 5. Crear directorio de trabajo para el proyecto
mkdir -p /opt/solid-octo-fiesta
chown -R ubuntu:ubuntu /opt/solid-octo-fiesta || true

echo "✅ Aprovisionamiento completado con éxito."
