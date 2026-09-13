# Infraestructura en Google Cloud Platform (GCP)

Overview de la infraestructura aprovisionada mediante Terraform en GCP, destacando la red VPC, políticas de seguridad, recursos de almacenamiento y la máquina virtual Compute Engine de bajo costo.

## 1. Topología de Infraestructura en GCP

```mermaid
flowchart TB
    subgraph ADMIN[Administración & IaC]
        TF[Terraform CLI]
        GCS[(GCS Bucket: tfstate<br/>Versioning: Habilitado)]
        TF -->|Almacena estado remoto| GCS
    end

    subgraph INTERNET[Tráfico Externo]
        USERS[Usuarios / Jugadores]
    end

    subgraph GCP_PROJECT[Google Cloud Platform - Proyecto]
        direction TB

        STATIC_IP[IP Pública Estática<br/>google_compute_address]
        USERS -->|HTTP / HTTPS| STATIC_IP

        subgraph VPC[VPC Network: solid-octo-dev-vpc]
            FW[Reglas de Firewall<br/>Puertos: 22, 80, 443, 3000, 8000]
            STATIC_IP --> FW

            subgraph SUBNET[Subred: solid-octo-dev-subnet<br/>CIDR: 10.10.1.0/24]
                
                subgraph VM[Compute Engine VM: solid-octo-dev-vm]
                    direction TB
                    SA[Service Account Dedicada<br/>Principle of Least Privilege]
                    DISK[(Disco 25GB<br/>pd-balanced)]
                    SWAP[Memoria Swap 2GB<br/>Optimización OOM]

                    subgraph DOCKER[Docker Engine & Compose Stack]
                        FRONT[Frontend Nuxt 4 :3000]
                        GW[API Gateway Nginx :8000]
                        SVC1[Identity Service :8001]
                        SVC2[Game Service :8002]
                        SVC3[Shop Service :8003]
                        SVC4[Leaderboard Service :8004]
                        DB[(PostgreSQL 16 Multi-DB :5432)]
                        CACHE[(Redis 7 Pub/Sub :6379)]
                    end
                end
            end
        end
    end

    FW -->|Tráfico filtrado por tags| VM
```

## 2. Mapa de Servicios GCP Utilizados

```mermaid
flowchart LR
    subgraph SERVICIOS_GCP[Servicios de Google Cloud Utilizados]
        GCE[Google Compute Engine<br/>VM e2-small / Ubuntu 22.04]
        VPC_SVC[Google Cloud VPC<br/>Red y Subred dedicada]
        GCS_SVC[Google Cloud Storage<br/>Bucket de tfstate con versionado]
        IAM_SVC[Google Cloud IAM<br/>Cuenta de servicio personalizada]
        ADDR_SVC[Cloud External IP<br/>Dirección IPv4 pública estática]
    end

    GCE --- VPC_SVC
    GCE --- ADDR_SVC
    GCE --- IAM_SVC
    GCS_SVC -.->|Estado IaC| GCE
```
