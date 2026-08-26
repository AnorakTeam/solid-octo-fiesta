# Proceso de juego y sincronización

**Razón de existir:** muestra el recorrido de una persona desde el registro hasta el ranking y, sobre todo, dónde se producen las escrituras de puntuación. Esto hace visible que la puntuación se calcula localmente y se persiste con sincronizaciones periódicas.

```mermaid
sequenceDiagram
    autonumber
    actor J as Jugador
    participant F as Frontend Nuxt 4 con Pinia
    participant B as API Django con DRF
    participant D as PostgreSQL

    J->>F: Registro (email y contraseña)
    F->>B: POST /api/v1/auth/register
    B->>D: Crear User y PlayerProgress(score=0)
    D-->>B: Entidades creadas
    B-->>F: 201 Usuario creado

    J->>F: Inicio de sesión
    F->>B: POST /api/v1/auth/login
    B-->>F: access JWT + refresh JWT
    Note over F: Guarda los tokens en cookies legibles por Nuxt

    J->>F: Abrir /game
    F->>F: Middleware restaura el access JWT si hace falta
    par Cargar estado inicial
        F->>B: GET /api/v1/game/state (Bearer JWT)
        B->>D: Consultar PlayerProgress del usuario
        D-->>B: score y updated_at
        B-->>F: Estado del progreso
    and Cargar mejoras
        F->>B: GET /api/v1/game/upgrades (Bearer JWT)
        B->>D: Consultar PlayerUpgrade del usuario
        D-->>B: Cantidades de mejoras
        B-->>F: Catálogo con cantidades y producción
    end

    loop Cada click e ingreso pasivo local
        J->>F: Click en +1
        F->>F: Incrementar score local
    end

    loop Cada 30 segundos, al salir o cerrar la página
        F->>B: POST /api/v1/game/sync {score} (Bearer JWT)
        B->>D: Guardar max(score recibido, score persistido)
        D-->>B: Progreso actualizado
        B-->>F: score y updated_at
    end

    opt Comprar una mejora
        J->>F: Elegir mejora
        F->>B: POST /api/v1/game/sync
        F->>B: POST /api/v1/game/upgrades/:key/purchase
        B->>D: Transacción: bloquear progreso y descontar puntos
        B->>D: Aumentar cantidad de PlayerUpgrade
        D-->>B: Compra confirmada
        B-->>F: score, mejoras y producción actualizados
    end

    J->>F: Consultar ranking
    F->>B: GET /api/v1/game/leaderboard
    Note over F,B: Endpoint público; no requiere JWT
    B->>D: Ordenar PlayerProgress por score y nickname
    D-->>B: Top 20 con datos de usuario
    B-->>F: Ranking
```

El cliente no envía cada click individualmente: agrupa el avance en el estado local y lo sincroniza. La API evita que una sincronización atrasada reduzca una puntuación ya guardada, usando el mayor valor entre ambos scores.
