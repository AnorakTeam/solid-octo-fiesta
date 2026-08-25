# solid-octo-fiesta

MVP clicker/idle con Nuxt 4 + TailwindCSS y Django REST Framework.

## Arranque rápido

```bash
docker compose up -d db
cd backend && python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver
```

En otra terminal:

```bash
cd frontend && npm install && npm run dev
```

La API queda en `http://localhost:8000` y Nuxt en `http://localhost:3000`.

## API

`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/users/me`, `GET /api/v1/game/state`, `POST /api/v1/game/sync` y `GET /api/v1/game/leaderboard`.

