# server/Dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# RUN python manage.py makemigrations
# RUN python manage.py migrate


CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]
