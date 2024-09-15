docker compose build
docker compose run server python manage.py makemigrations upload_video
docker compose run server python manage.py migrate
docker compose up 


