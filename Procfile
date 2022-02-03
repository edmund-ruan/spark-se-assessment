#web: gunicorn wsgi:app

heroku ps:scale web=1

web: ./launch.sh

#release: python project.server.__init__.py db upgrade