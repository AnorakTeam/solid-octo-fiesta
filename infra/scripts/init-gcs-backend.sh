#!/usr/bin/env bash
set -e

# ==============================================================================
# Script de Creación de Bucket GCS para Backend Remoto de Terraform
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================================="
echo "   Inicializador de Bucket GCS para Estado de Terraform"
echo "=========================================================="

# 1. Verificar si gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: Google Cloud SDK ('gcloud') no está instalado o no está en el PATH."
    echo "   Por favor instálalo o inicia sesión antes de continuar."
    exit 1
fi

# 2. Obtener el ID del proyecto
PROJECT_ID="${GCP_PROJECT_ID:-}"

# Si no está en variable de entorno, intentar leerlo de terraform.tfvars si existe
if [ -z "$PROJECT_ID" ] && [ -f "${INFRA_DIR}/terraform.tfvars" ]; then
    PROJECT_ID=$(grep -E '^\s*gcp_project_id\s*=' "${INFRA_DIR}/terraform.tfvars" | sed -E 's/.*=\s*"([^"]+)".*/\1/' || true)
fi

# Si aún no se tiene, intentar obtenerlo de la configuración activa de gcloud
if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null || true)
fi

# Solicitar al usuario si aún está vacío
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
    echo "ℹ️  No se detectó un proyecto configurado en gcloud."
    read -rp "Ingresa tu ID de proyecto de GCP: " PROJECT_ID
fi

REGION="${GCP_REGION:-us-central1}"
APP_NAME="${APP_NAME:-solid-octo}"

# Nombre único para el bucket (los nombres de buckets son globales en GCP)
BUCKET_NAME="tfstate-${PROJECT_ID}-${APP_NAME}"

echo ""
echo "📋 Parámetros detectados:"
echo "   - Proyecto:  ${PROJECT_ID}"
echo "   - Región:    ${REGION}"
echo "   - Bucket:    ${BUCKET_NAME}"
echo ""

# 3. Comprobar si el bucket ya existe
echo "🔍 Verificando existencia del bucket gs://${BUCKET_NAME}..."
if gcloud storage buckets describe "gs://${BUCKET_NAME}" --project="${PROJECT_ID}" &>/dev/null; then
    echo "✅ El bucket gs://${BUCKET_NAME} ya existe en tu proyecto."
else
    echo "🚀 Creando bucket gs://${BUCKET_NAME} en ${REGION}..."
    gcloud storage buckets create "gs://${BUCKET_NAME}" \
        --project="${PROJECT_ID}" \
        --location="${REGION}" \
        --uniform-bucket-level-access

    echo "🛡️  Habilitando versionado de objetos (para prevenir pérdida de tfstate)..."
    gcloud storage buckets update "gs://${BUCKET_NAME}" --versioning
    echo "✅ Bucket creado y protegido exitosamente."
fi

# 4. Generar configuración para backend.tf
BACKEND_FILE="${INFRA_DIR}/backend.tf"

echo ""
echo "=========================================================="
echo "   Configuración lista para infra/backend.tf"
echo "=========================================================="
cat <<EOF

terraform {
  backend "gcs" {
    bucket = "${BUCKET_NAME}"
    prefix = "${APP_NAME}/state"
  }
}

EOF

read -rp "¿Deseas actualizar automáticamente infra/backend.tf con esta configuración? (s/n): " APPLY_CONF

if [[ "$APPLY_CONF" =~ ^[sS](i|I)?$ ]]; then
    cat <<EOF > "${BACKEND_FILE}"
# Generado automáticamente por scripts/init-gcs-backend.sh
terraform {
  backend "gcs" {
    bucket = "${BUCKET_NAME}"
    prefix = "${APP_NAME}/state"
  }
}
EOF
    echo "✅ ${BACKEND_FILE} actualizado exitosamente."
    echo "💡 Ahora puedes ejecutar en la carpeta 'infra':"
    echo "   terraform init -migrate-state"
else
    echo "ℹ️  Puedes copiar el bloque anterior y pegarlo manualmente en ${BACKEND_FILE}."
fi
