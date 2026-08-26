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

## Despliegue

Backend (`solid-octo-fiesta.vercel.app`):

```text
DJANGO_SECRET_KEY=<secreto-aleatorio>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=solid-octo-fiesta.vercel.app
DATABASE_URL=<connection-string-de-supabase>
```

En Supabase, copia la cadena de conexión PostgreSQL desde **Project Settings > Database > Connection string**. Usa el modo **Session pooler** si tu proveedor serverless limita las conexiones. Configura `DATABASE_URL` como variable de entorno en Vercel y ejecuta las migraciones antes del primer uso:

```bash
cd backend
DATABASE_URL="<connection-string-de-supabase>" python manage.py migrate
```

Frontend (`solid-octo-fiesta-game.vercel.app`):

```text
NUXT_PUBLIC_API_BASE=https://solid-octo-fiesta.vercel.app/api/v1
```

Después de cambiar `NUXT_PUBLIC_API_BASE`, hacer redeploy del frontend: Nuxt incorpora las variables `NUXT_PUBLIC_*` durante el build. El backend permite CORS desde cualquier origen y usa JWT en el header `Authorization`; no usa cookies cross-site.

## API

`POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`, `POST /api/v1/auth/logout`, `GET /api/v1/users/me`, `PATCH /api/v1/users/me/profile`, `GET /api/v1/game/state`, `POST /api/v1/game/sync`, `GET /api/v1/game/leaderboard`, `GET /api/v1/game/upgrades` y `POST /api/v1/game/upgrades/:key/purchase`.

### Perfil 

`PATCH /api/v1/users/me/profile` usa autenticación JWT y acepta `multipart/form-data`:

```text
nickname: nuevo_nombre
profile_icon: archivo opcional (JPG, PNG o WebP; máximo 2 MB)
```

El endpoint identifica al jugador mediante el JWT y solamente actualiza su entidad `User`; su `PlayerProgress` y score no se modifican.
