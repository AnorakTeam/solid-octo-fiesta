# ==============================================================================
# Terraform Remote Backend (Google Cloud Storage)
# ==============================================================================
# Por defecto, Terraform inicia con estado local (local backend).
# Para almacenar el tfstate en GCP Storage de manera segura y colaborativa:
# 1. Ejecuta el script: bash scripts/init-gcs-backend.sh
# 2. Descomenta el bloque a continuación y coloca el nombre de tu bucket.
# 3. Ejecuta: terraform init -migrate-state
# ==============================================================================

# terraform {
#   backend "gcs" {
#     bucket = "REEMPLAZAR_CON_TU_BUCKET_TFSTATE"
#     prefix = "solid-octo-fiesta/state"
#   }
# }
