web: gunicorn wsgi:app

heroku ps:scale web=1

release: python ../server.__init__.py db upgrade
