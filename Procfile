web: gunicorn manage:app
heroku ps:scale web=1


web: gunicorn app:app
release: python manage.py db upgrade
