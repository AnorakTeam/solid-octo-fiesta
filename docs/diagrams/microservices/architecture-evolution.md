# Evolución de la Arquitectura: Monolito vs Microservicios

Comparativa de alto nivel entre la arquitectura monolítica original y la arquitectura actual desacoplada en microservicios independientes orientada a eventos.

## 1. Estado Anterior: Backend Monolítico

```mermaid
flowchart LR
    J[Jugadores] --> F[Frontend Nuxt 4]
    F -->|JWT + REST :8000| M

    subgraph M[Monolito Django + DRF]
        direction TB
        A[Autenticación y Perfil]
        G[Estado de Juego y Sync]
        U[Compras y Mejoras]
        R[Ranking / Leaderboard]
        A --- G --- U --- R
    end

    M --> DB[(Base de Datos Única PostgreSQL)]
    DB --- T1[(auth_user)]
    DB --- T2[(player_progress)]
    DB --- T3[(player_upgrade)]
```

## 2. Nuevo Estado Actual: Microservicios Desacoplados

```mermaid
flowchart LR
    J[Jugadores] --> F[Frontend Nuxt 4 :3000]
    F -->|REST /api/v1| GW[API Gateway / Nginx :8000]

    subgraph SERVICES[Capa de Microservicios Django Independientes]
        direction TB
        ID[Identity Service :8001]
        GAME[Game Service :8002]
        SHOP[Shop Service :8003]
        BOARD[Leaderboard Service :8004]
    end

    GW -->|/auth/*, /users/*| ID
    GW -->|/game/state, /game/sync| GAME
    GW -->|/game/upgrades*| SHOP
    GW -->|/game/leaderboard| BOARD

    ID --> ID_DB[(identity_db)]
    GAME --> GAME_DB[(game_db)]
    SHOP --> SHOP_DB[(shop_db)]
    BOARD --> BOARD_DB[(leaderboard_db)]

    GAME -.->|score_updated| REDIS[(Redis Event Bus)]
    ID -.->|profile_updated| REDIS
    REDIS -.->|proyección asíncrona| BOARD
    SHOP <-->|descuento atómico interno| GAME
```
