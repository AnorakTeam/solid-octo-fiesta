# Arquitectura Detallada del Backend y Bases de Datos

Detalle de interacción entre los microservicios Django, sus bases de datos PostgreSQL aisladas, el bus de eventos en Redis y el modelo de datos desacoplado por `user_id`.

## 1. Flujo de Comunicación e Integración de Servicios

```mermaid
flowchart TB
    Client[Cliente / Frontend Nuxt 4] -->|HTTP REST| GW[API Gateway / Nginx :8000]

    %% Enrutamiento Gateway
    GW -->|/api/v1/auth/*<br/>/api/v1/users/*| ID[identity-service :8001]
    GW -->|/api/v1/game/state<br/>/api/v1/game/sync| GAME[game-service :8002]
    GW -->|/api/v1/game/upgrades*| SHOP[shop-service :8003]
    GW -->|/api/v1/game/leaderboard| BOARD[leaderboard-service :8004]

    %% Bases de Datos
    subgraph POSTGRES[Instancia PostgreSQL 16]
        ID_DB[(identity_db)]
        GAME_DB[(game_db)]
        SHOP_DB[(shop_db)]
        BOARD_DB[(leaderboard_db)]
    end

    ID -->|ORM Django| ID_DB
    GAME -->|ORM Django| GAME_DB
    SHOP -->|ORM Django| SHOP_DB
    BOARD -->|ORM Django| BOARD_DB

    %% Comunicación Interna
    SHOP -->|POST /internal/deduct-points<br/>Header: X-Internal-Secret| GAME

    %% Eventos Redis
    subgraph REDIS[Redis 7 Pub/Sub]
        E_USER[Canal: user_events]
        E_GAME[Canal: game_events]
    end

    ID -.->|evento: profile_updated<br/>evento: user_registered| E_USER
    GAME -.->|evento: score_updated| E_GAME

    subgraph WORKER[Leaderboard Projection Worker]
        CONSUMER[run_event_consumer.py]
    end

    E_USER -.-> CONSUMER
    E_GAME -.-> CONSUMER
    CONSUMER -->|Actualiza proyección| BOARD_DB
```

## 2. Modelo de Datos Desacoplado (Sin Foreign Keys entre Servicios)

```mermaid
erDiagram
    %% Identity DB
    CUSTOM_USER {
        bigint id PK
        string email UK
        string nickname UK
        string profile_icon
        datetime created_at
    }

    %% Game DB
    PLAYER_PROGRESS {
        bigint id PK
        bigint user_id UK "Desacoplado (Claim JWT)"
        bigint score
        datetime updated_at
    }

    %% Shop DB
    PLAYER_UPGRADE {
        bigint id PK
        bigint user_id "Desacoplado (Claim JWT)"
        string upgrade_type
        int quantity
        datetime updated_at
    }

    %% Leaderboard DB
    LEADERBOARD_ENTRY {
        bigint id PK
        bigint user_id UK "Desacoplado (Id Proyectado)"
        string nickname
        bigint score
        string profile_icon
        datetime updated_at
    }

    CUSTOM_USER -.->|"user_id (vía JWT)"| PLAYER_PROGRESS
    CUSTOM_USER -.->|"user_id (vía JWT)"| PLAYER_UPGRADE
    PLAYER_PROGRESS -.->|"evento asíncrono"| LEADERBOARD_ENTRY
```
