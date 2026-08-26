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

`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/users/me`, `PATCH /api/v1/users/me/profile`, `GET /api/v1/game/state`, `POST /api/v1/game/sync` y `GET /api/v1/game/leaderboard`.

### Perfil

`PATCH /api/v1/users/me/profile` usa autenticación JWT y acepta `multipart/form-data`:

```text
nickname: nuevo_nombre
profile_icon: archivo opcional (JPG, PNG o WebP; máximo 2 MB)
```

El endpoint identifica al jugador mediante el JWT y solamente actualiza su entidad `User`; su `PlayerProgress` y score no se modifican.
