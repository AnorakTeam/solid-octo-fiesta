FROM python:3.12-slim

# Por ahora se dejará sqlite para no complicar el deployment
# la principal preocupación realmente es el almacenamiento 
# de las imágenes de perfil, pero por ahora con esto es suficiente
# para el MVP.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=0 \
    DB_ENGINE=sqlite \
    PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN python manage.py migrate --noinput

EXPOSE 8000
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]
