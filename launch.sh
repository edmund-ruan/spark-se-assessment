#!/bin/bash

export FLASK_APP=project.server
export APP_SETTINGS="project.server.config.DevelopmentConfig"

APP_PORT=${PORT:-5000}

flask db init
flask db migrate
flask db upgrade
flask run --host=0.0.0.0 --port=APP_PORT
#flask run