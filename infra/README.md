# ☁️ Infraestructura en Google Cloud Platform (GCP) con Terraform

Esta carpeta contiene la configuración completa de infraestructura como código (**IaC**) con **Terraform** para desplegar la arquitectura de microservicios de **Solid Octo Fiesta** en una máquina virtual de bajo costo en **Google Compute Engine (GCE)** con una **IP pública estática**.

---

## 🏗️ Arquitectura Desplegada

```text
[ Internet / Usuarios ]
         │
         ▼
[ IP Pública Estática (Google Compute Address) ]
         │
         ▼
[ Firewall VPC (Puertos: 22 SSH, 80/443 Web, 3000 Frontend, 8000 Gateway) ]
         │
         ▼
[ VM Compute Engine (Ubuntu 22.04 LTS) ]
  ├── 💾 Swap File (2 GB para optimizar RAM en VMs económicas)
  ├── 🐳 Docker Engine + Docker Compose Plugin
  └── 📦 Contenedores de la aplicación:
        ├── Nuxt 4 Frontend (Puerto 3000)
        ├── Nginx API Gateway (Puerto 8000)
        ├── Identity Service (8001)
        ├── Game Service (8002)
        ├── Shop Service (8003)
        ├── Leaderboard Service (8004)
        ├── PostgreSQL 16 (4 bases de datos)
        └── Redis 7 (Message Bus)
```

---

## 💰 Optimización de Costos (Free Tier / Créditos)

- **Tipo de máquina recomendada:** `e2-small` (2 vCPUs, 2 GB RAM). 
  - El script de inicio (`startup.sh`) configura automáticamente un archivo de **Swap de 2GB**, permitiendo que la máquina ejecute Docker Compose sin problemas de memoria (OOM).
  - Costo aproximado: ~$14 USD/mes (o cubierto por créditos de prueba de GCP).
- **Disco de arranque:** 25 GB `pd-balanced` o `pd-standard` (GCP Free Tier incluye hasta 30 GB de disco estándar al mes).
- **Región recomendada:** `us-central1` (una de las regiones más económicas y con disponibilidad de Free Tier).
- **IP Estática:** Gratuita mientras esté asociada a una instancia de VM en ejecución.

---

## 📋 Prerrequisitos

1. **Google Cloud SDK (`gcloud` CLI)** instalado:
   ```bash
   gcloud --version
   ```
2. **Terraform** (versión >= 1.5.0) instalado:
   ```bash
   terraform --version
   ```
3. Una cuenta de GCP con un proyecto activo y facturación habilitada (créditos o tarjeta).

---

## 🚀 Guía de Despliegue Paso a Paso

### 1. Autenticarse en Google Cloud

Inicia sesión y genera las credenciales de aplicación local para que Terraform pueda interactuar con tu cuenta:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project TU_PROJECT_ID_AQUI
```

Habilita las APIs necesarias en tu proyecto:

```bash
gcloud services enable compute.googleapis.com storage.googleapis.com
```

---

### 2. Configurar el Bucket de Estado Remoto (`tfstate`)

Para guardar el estado de Terraform de forma segura y colaborativa en Google Cloud Storage (GCS), ejecuta el script provisto:

```bash
cd infra
bash scripts/init-gcs-backend.sh
```

El script:
1. Detectará tu proyecto de GCP.
2. Creará un bucket `gs://tfstate-<PROJECT_ID>-solid-octo` con protección de versionado.
3. Te preguntará si deseas activar automáticamente la configuración en `backend.tf`.

*(Si prefieres probar primero con estado local en tu máquina, puedes saltarte este paso y dejar `backend.tf` comentado).*

---

### 3. Configurar Variables

Copia el archivo de ejemplo de variables y edita `gcp_project_id`:

```bash
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars
```

Asegúrate de definir al menos:
```hcl
gcp_project_id = "tu-proyecto-gcp-id"
```

---

### 4. Inicializar y Aplicar Terraform

Desde el directorio `infra/`:

```bash
# Inicializar proveedores y backend
terraform init

# Ver el plan de recursos a crear
terraform plan

# Desplegar la infraestructura
terraform apply -auto-approve
```

Al terminar, Terraform imprimirá los outputs con la **IP pública estática**:

```text
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:

frontend_url = "http://34.123.45.67:3000"
gateway_api_url = "http://34.123.45.67:8000/api/v1"
public_ip = "34.123.45.67"
ssh_connection_command = "gcloud compute ssh --zone us-central1-a solid-octo-dev-vm --project tu-proyecto"
vm_instance_name = "solid-octo-dev-vm"
```

---

### 5. Desplegar los Microservicios en la VM

Conéctate a la nueva instancia usando el comando de SSH provisto en el output:

```bash
gcloud compute ssh --zone us-central1-a solid-octo-dev-vm
```

Una vez dentro de la VM:

1. **Clonar tu repositorio:**
   ```bash
   cd /opt/solid-octo-fiesta
   git clone <URL_DE_TU_REPOSITORIO> .
   ```

2. **Configurar las variables de entorno con la IP pública de la VM:**
   ```bash
   # Configurar .env raíz
   cp .env.example .env

   # Configurar NUXT_PUBLIC_API_BASE con la IP pública de la VM
   PUBLIC_IP=$(curl -s ifconfig.me)
   echo "NUXT_PUBLIC_API_BASE=http://${PUBLIC_IP}:8000/api/v1" >> frontend/.env
   ```

3. **Iniciar los microservicios:**
   ```bash
   bash scripts/start-local.sh
   ```

4. **Crear usuario administrador (opcional):**
   ```bash
   bash scripts/create-superuser.sh
   ```

---

### 6. ¡Listo para Probar!

Abre en tu navegador la URL con la IP pública:
- **Frontend del Juego:** `http://<TU_IP_PUBLICA>:3000`
- **API Gateway Health:** `http://<TU_IP_PUBLICA>:8000/api/v1/health`

Cualquier compañero o usuario externo podrá acceder directamente a la IP pública sin necesidad de configurar dominios o certificados SSL por el momento.

---

## 🧹 Destrucción de Recursos

Para no incurrir en costos una vez que termines de probar:

```bash
cd infra
terraform destroy -auto-approve
```
