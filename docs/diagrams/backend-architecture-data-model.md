# Arquitectura del backend y modelo de datos

**Razón de existir:** localiza las responsabilidades del monolito Django y documenta qué entidades intervienen en autenticación, progreso, compras y ranking. Sirve como referencia antes de modificar endpoints o migraciones.

## Arquitectura backend

```mermaid
flowchart TB
    C[Cliente Nuxt] -->|HTTP /api/v1| U[config.urls]
    U --> H[GET /health]
    U --> A[apps.accounts]
    U --> G[apps.game]

    A --> AV[Views: register, login, refresh,<br/>logout, me y profile]
    AV --> AS[Serializers y validación]
    AS --> AU[User personalizado]
    AV --> JWT[Simple JWT]

    G --> GV[Views: state, sync,<br/>leaderboard y upgrades]
    GV --> GS[Serializers]
    GV --> UC[Catálogo de mejoras en código]
    GV --> GP[PlayerProgress]
    GV --> GU[PlayerUpgrade]
    GV --> TX[Transacción y bloqueos<br/>en compra]

    AU --> DB[(PostgreSQL)]
    GP --> DB
    GU --> DB
    TX --> DB
    AV --> M[Media: profile_icons/]
    M --> FI[Archivo de icono de perfil]
```

El `User` personalizado identifica al jugador por correo. `apps.accounts` crea el progreso inicial durante el registro; `apps.game` centraliza el estado, las sincronizaciones y las compras. El catálogo de tipos, precios y producción de mejoras (`clicker`, `static`, `spammer`) vive actualmente en código y las cantidades compradas viven en la base de datos.

## Modelo de datos relevante

```mermaid
erDiagram
    USER ||--|| PLAYER_PROGRESS : posee
    USER ||--o{ PLAYER_UPGRADE : compra

    USER {
        bigint id PK
        string email UK
        string nickname UK
        string password_hash
        string profile_icon
        boolean is_active
        boolean is_staff
        datetime date_joined
    }

    PLAYER_PROGRESS {
        bigint id PK
        bigint user_id FK
        bigint score
        datetime created_at
        datetime updated_at
    }

    PLAYER_UPGRADE {
        bigint id PK
        bigint user_id FK
        string upgrade_type "clicker | static | spammer"
        integer quantity
        datetime updated_at
    }
```

| Tabla | Propósito y reglas importantes |
| --- | --- |
| `accounts_user` | Cuenta del jugador. `email` y `nickname` son únicos; el icono de perfil es opcional. |
| `game_playerprogress` | Estado persistente del juego. Existe exactamente un registro por usuario (`user_id` uno a uno) y conserva el `score` más reciente. |
| `game_playerupgrade` | Cantidad adquirida de cada tipo de mejora por jugador. La combinación (`user_id`, `upgrade_type`) es única; la compra bloquea las filas dentro de una transacción para descontar puntos y aumentar la cantidad de forma atómica. |
