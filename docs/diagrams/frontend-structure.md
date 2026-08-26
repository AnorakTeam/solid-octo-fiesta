# Estructura del frontend

**Razón de existir:** explica cómo Nuxt organiza las rutas, el estado de sesión y el estado de juego, y qué piezas son responsables de invocar la API. Facilita mantener separada la lógica del juego de la interfaz.

```mermaid
flowchart TB
    APP[app.vue<br/>fondo, logo y NuxtPage] --> PAGES

    subgraph PAGES[Pages / rutas]
        HOME[/ /]
        LOGIN[/login]
        REGISTER[/register]
        GAME[/game<br/>requiere auth]
        PROFILE[/profile<br/>requiere auth]
        LEADERBOARD[/leaderboard]
    end

    GAME --> GM[useGameStore]
    GAME --> AU[useAuthStore]
    PROFILE --> AU
    LOGIN --> AU
    REGISTER --> REG[POST /auth/register]
    LEADERBOARD --> LB[GET /game/leaderboard]

    subgraph COMPONENTS[Componentes de interfaz]
        TOP[GameTopRankings]
        UP[GameUpgradesPanel]
        FX[FloatingNumberSpawner<br/>y ScoreMilestoneConfetti]
        VIS[FloatingBubbleBackground<br/>y FloatingSiteLogo]
    end

    APP --> VIS
    GAME --> TOP
    GAME --> UP
    GAME --> FX
    LOGIN --> TOP
    GM --> UP

    MW[Middleware auth] --> AU
    GAME --> MW
    PROFILE --> MW

    AU --> TOK[Cookies: access y refresh JWT]
    AU --> API[apiFetch: Bearer JWT,<br/>refresh automático ante 401]
    GM --> API
    REG --> API
    LB --> API
    TOP --> API
    API --> BACKEND[Django REST API]
```

`useAuthStore` gestiona los JWT, el perfil y la renovación del access token. `useGameStore` conserva el score y las mejoras en memoria, calcula la producción pasiva y sincroniza el score. La página de juego ejecuta esa sincronización cada 30 segundos, al abandonar la ruta y durante `pagehide`; antes de una compra también sincroniza el puntaje.

Las rutas `/game` y `/profile` pasan por el middleware `auth`; `/leaderboard` es pública. Los componentes de ranking hacen consultas públicas directamente, mientras que las operaciones de sesión y juego usan el método autenticado `apiFetch`.
