chmod u+x launch.sh && ./launch.sh

web: gunicorn user-login-app-by-edmundr:app
heroku ps:scale web=1

release: python migrations/env.py db upgrade